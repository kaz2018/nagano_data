function parseKidsCsv(text) {
  const lines = text.replace(/^\uFEFF/, '').trim().split(/\r?\n/).filter(Boolean);
  const headers = lines[0].split(',');
  return lines.slice(1).map((line) => {
    const values = line.split(',');
    return headers.reduce((row, header, index) => {
      row[header] = values[index];
      return row;
    }, {});
  });
}

async function loadKidsCsv(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to load CSV: ${url}`);
  }
  return parseKidsCsv(await response.text());
}

function formatKidsNumber(value) {
  return Number(value).toLocaleString('ja-JP');
}

async function initKidsSortableTable({
  csvUrl,
  headId,
  bodyId,
  columns,
  transformRow = (row) => row,
  theme,
  defaultSort = null,
}) {
  const sourceRows = await loadKidsCsv(csvUrl);
  const rows = sourceRows.map((row, index) => transformRow(row, index, sourceRows));
  const headRow = document.getElementById(headId);
  const body = document.getElementById(bodyId);
  const sortState = {
    key: defaultSort ? defaultSort.key : null,
    direction: defaultSort ? defaultSort.direction : null,
  };
  const numberColumns = columns.filter((column) => column.type === 'number');
  const maxByKey = Object.fromEntries(
    numberColumns.map((column) => [column.key, Math.max(...rows.map((row) => Number(row[column.key])))])
  );

  function firstDirectionFor(type) {
    return type === 'number' ? 'desc' : 'asc';
  }

  function nextDirection(key, type) {
    const firstDirection = firstDirectionFor(type);
    const secondDirection = firstDirection === 'desc' ? 'asc' : 'desc';
    if (sortState.key !== key) return firstDirection;
    if (sortState.direction === firstDirection) return secondDirection;
    return null;
  }

  function currentRows() {
    if (!sortState.key || !sortState.direction) {
      return rows;
    }

    const sortColumn = columns.find((column) => column.key === sortState.key);
    const sortedRows = [...rows];
    sortedRows.sort((a, b) => {
      const comparison = sortColumn.type === 'number'
        ? Number(a[sortColumn.key]) - Number(b[sortColumn.key])
        : String(a[sortColumn.key]).localeCompare(String(b[sortColumn.key]), 'ja');
      return sortState.direction === 'desc' ? -comparison : comparison;
    });
    return sortedRows;
  }

  function sortArrow(column) {
    if (sortState.key !== column.key || !sortState.direction) return '';
    return sortState.direction === 'desc' ? '▼' : '▲';
  }

  function render() {
    headRow.innerHTML = columns.map((column) => `
      <th class="px-2 py-2 text-${column.align}">
        <button
          type="button"
          data-col-key="${column.key}"
          data-col-type="${column.type}"
          class="w-full font-bold flex items-center ${column.align === 'left' ? 'justify-start' : 'justify-end'} gap-1 hover:underline"
        >
          <span>${column.label}</span>
          <span class="text-xs">${sortArrow(column)}</span>
        </button>
      </th>
    `).join('');

    body.innerHTML = currentRows().map((row) => `
      <tr class="border-t ${theme.rowBorderClass} ${theme.rowHoverClass}">
        ${columns.map((column) => {
          const value = column.render
            ? column.render(row[column.key], row)
            : column.type === 'number'
              ? formatKidsNumber(row[column.key])
              : row[column.key];
          const highlightClass = column.type === 'number' && Number(row[column.key]) === maxByKey[column.key]
            ? theme.maxCellClass
            : '';
          const baseClass = column.align === 'left'
            ? 'px-3 py-2 text-left font-bold text-gray-700'
            : 'px-3 py-2 text-right text-gray-600';
          return `<td class="${baseClass} ${highlightClass}">${value}</td>`;
        }).join('')}
      </tr>
    `).join('');
  }

  headRow.addEventListener('click', (event) => {
    const trigger = event.target.closest('button[data-col-key]');
    if (!trigger) return;

    const { colKey, colType } = trigger.dataset;
    const direction = nextDirection(colKey, colType);
    sortState.key = direction ? colKey : null;
    sortState.direction = direction;
    render();
  });

  render();
}

async function initKidsBarChart({
  csvUrl,
  containerId,
  sortButtonId,
  transformRows,
  theme,
  defaultSorted = false,
}) {
  const rows = transformRows(await loadKidsCsv(csvUrl));
  const maxValue = Math.max(...rows.map((row) => Number(row.value)));
  const maxCityValue = Math.max(...rows.filter((row) => row.type === 'city').map((row) => Number(row.value)));
  let sorted = defaultSorted;

  function render() {
    const chart = document.getElementById(containerId);
    const button = document.getElementById(sortButtonId);
    const displayRows = sorted ? [...rows].sort((a, b) => b.value - a.value) : rows;
    button.textContent = sorted ? 'もとのじゅんにもどす' : '人口が多いじゅんにならべる';
    chart.innerHTML = displayRows.map((row) => {
      const percent = (Number(row.value) / maxValue) * 100;
      const isMaxCity = row.type === 'city' && Number(row.value) === maxCityValue;
      const barColor = isMaxCity
        ? theme.maxBarClass
        : row.type === 'village'
          ? theme.villageBarClass
          : theme.cityBarClass;
      const labelColor = row.type === 'village' ? 'text-gray-500' : 'text-gray-700';
      const showInside = percent > 22;
      return `
        <div class="flex items-center gap-2">
          <div class="w-20 shrink-0 text-right text-xs font-bold ${labelColor}">${row.name}</div>
          <div class="flex-1 flex items-center">
            <div class="${barColor} h-6 rounded-r flex items-center justify-end pr-2 transition-all duration-500"
              style="width: ${Math.max(percent, 0.6)}%">
              ${showInside ? `<span class="text-white text-xs font-bold">${formatKidsNumber(row.value)}</span>` : ''}
            </div>
            ${showInside ? '' : `<span class="text-xs text-gray-500 ml-1">${formatKidsNumber(row.value)}</span>`}
          </div>
        </div>
      `;
    }).join('');
  }

  document.getElementById(sortButtonId).addEventListener('click', () => {
    sorted = !sorted;
    render();
  });

  render();
}

function moveKidsSectionsAfter({ markerId, sectionIds }) {
  const marker = document.getElementById(markerId);
  const fragment = document.createDocumentFragment();
  sectionIds
    .map((id) => document.getElementById(id))
    .filter(Boolean)
    .forEach((section) => fragment.appendChild(section));
  marker.after(fragment);
}
