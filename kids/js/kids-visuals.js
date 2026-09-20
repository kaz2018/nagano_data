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
  rows: providedRows = null,
  headId,
  bodyId,
  columns,
  transformRow = (row) => row,
  theme,
  defaultSort = null,
}) {
  const sourceRows = providedRows || await loadKidsCsv(csvUrl);
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

// --- ペンギン研究所 共通 ------------------------------------------------

// しゅるいの色はレッスンをまたいで固定する（P4以降）
const KIDS_SPECIES_COLORS = {
  'アデリーペンギン': '#4f46e5',
  'ヒゲペンギン': '#db2777',
  'ジェンツーペンギン': '#0891b2',
};

// 最小二乗法で直線をもとめる（ちらばりグラフの「だいたいの向き」用）
function kidsLinearFit(points) {
  const n = points.length;
  if (n < 2) return null;
  const sumX = points.reduce((total, p) => total + p.x, 0);
  const sumY = points.reduce((total, p) => total + p.y, 0);
  const sumXX = points.reduce((total, p) => total + p.x * p.x, 0);
  const sumXY = points.reduce((total, p) => total + p.x * p.y, 0);
  const denominator = n * sumXX - sumX * sumX;
  if (denominator === 0) return null;
  const slope = (n * sumXY - sumX * sumY) / denominator;
  return { slope, intercept: (sumY - slope * sumX) / n };
}

/**
 * ちらばりグラフ（散布図）を SVG で描く。
 * Tailwind の色クラスは実行時生成だと効かないので、色は必ず16進で受け取る。
 *
 * points     : [{ x, y, group, label? }]
 * xAxis/yAxis: { min, max, step, label, format?(value) }
 * groups     : [{ key, color }]  凡例と色の対応
 * trend      : 'none' | 'all' | 'each'
 * onSelect   : (point, index) => void  点をタップしたときに呼ばれる
 */
function renderKidsScatter({
  containerId,
  points,
  xAxis,
  yAxis,
  groups,
  visibleGroups = null,
  trend = 'none',
  trendColor = '#94a3b8',
  pointRadius = 4,
  onSelect = null,
}) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const width = 640;
  const height = 420;
  const pad = { left: 62, right: 16, top: 16, bottom: 48 };
  const plotWidth = width - pad.left - pad.right;
  const plotHeight = height - pad.top - pad.bottom;

  const toSvgX = (value) => pad.left + ((value - xAxis.min) / (xAxis.max - xAxis.min)) * plotWidth;
  const toSvgY = (value) => pad.top + plotHeight - ((value - yAxis.min) / (yAxis.max - yAxis.min)) * plotHeight;

  const colorOf = Object.fromEntries(groups.map((g) => [g.key, g.color]));
  const shown = points.filter((p) => !visibleGroups || visibleGroups.includes(p.group));
  container.kidsScatterPoints = shown;

  const ticks = (axis) => {
    const values = [];
    for (let v = axis.min; v <= axis.max + 1e-9; v += axis.step) values.push(Math.round(v * 1000) / 1000);
    return values;
  };
  const formatTick = (axis, value) => (axis.format ? axis.format(value) : String(value));

  const gridX = ticks(xAxis).map((v) => `
    <line x1="${toSvgX(v)}" y1="${pad.top}" x2="${toSvgX(v)}" y2="${pad.top + plotHeight}" stroke="#e2e8f0" stroke-width="1" />
    <text x="${toSvgX(v)}" y="${pad.top + plotHeight + 20}" text-anchor="middle" font-size="12" fill="#94a3b8">${formatTick(xAxis, v)}</text>
  `).join('');

  const gridY = ticks(yAxis).map((v) => `
    <line x1="${pad.left}" y1="${toSvgY(v)}" x2="${pad.left + plotWidth}" y2="${toSvgY(v)}" stroke="#e2e8f0" stroke-width="1" />
    <text x="${pad.left - 8}" y="${toSvgY(v) + 4}" text-anchor="end" font-size="12" fill="#94a3b8">${formatTick(yAxis, v)}</text>
  `).join('');

  const trendGroups = trend === 'each'
    ? groups.filter((g) => !visibleGroups || visibleGroups.includes(g.key)).map((g) => ({
        color: g.color,
        data: shown.filter((p) => p.group === g.key),
      }))
    : trend === 'all'
      ? [{ color: trendColor, data: shown }]
      : [];

  const trendLines = trendGroups.map(({ color, data }) => {
    const fit = kidsLinearFit(data);
    if (!fit) return '';
    const xStart = Math.min(...data.map((p) => p.x));
    const xEnd = Math.max(...data.map((p) => p.x));
    const clampY = (value) => Math.min(yAxis.max, Math.max(yAxis.min, value));
    return `<line x1="${toSvgX(xStart)}" y1="${toSvgY(clampY(fit.slope * xStart + fit.intercept))}"
                  x2="${toSvgX(xEnd)}" y2="${toSvgY(clampY(fit.slope * xEnd + fit.intercept))}"
                  stroke="${color}" stroke-width="3" stroke-linecap="round" stroke-dasharray="7 5" opacity="0.85" />`;
  }).join('');

  const dots = shown.map((p, index) => `
    <circle data-kids-point="${index}" cx="${toSvgX(p.x)}" cy="${toSvgY(p.y)}" r="${pointRadius}"
      fill="${colorOf[p.group] || '#94a3b8'}" fill-opacity="0.7" stroke="#ffffff" stroke-width="0.8"
      class="cursor-pointer hover:fill-opacity-100" />
  `).join('');

  container.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" class="w-full h-auto" role="img"
      aria-label="${xAxis.label} と ${yAxis.label} のちらばりグラフ">
      ${gridX}
      ${gridY}
      <line x1="${pad.left}" y1="${pad.top + plotHeight}" x2="${pad.left + plotWidth}" y2="${pad.top + plotHeight}" stroke="#cbd5e1" stroke-width="2" />
      <line x1="${pad.left}" y1="${pad.top}" x2="${pad.left}" y2="${pad.top + plotHeight}" stroke="#cbd5e1" stroke-width="2" />
      ${trendLines}
      ${dots}
      <text x="${pad.left + plotWidth / 2}" y="${height - 6}" text-anchor="middle" font-size="13" font-weight="bold" fill="#64748b">${xAxis.label}</text>
      <text x="14" y="${pad.top + plotHeight / 2}" text-anchor="middle" font-size="13" font-weight="bold" fill="#64748b"
        transform="rotate(-90 14 ${pad.top + plotHeight / 2})">${yAxis.label}</text>
    </svg>
  `;

  if (onSelect && !container.kidsScatterBound) {
    container.addEventListener('click', (event) => {
      const dot = event.target.closest('[data-kids-point]');
      if (!dot) return;
      const index = Number(dot.dataset.kidsPoint);
      onSelect(container.kidsScatterPoints[index], index);
    });
    container.kidsScatterBound = true;
  }
}
