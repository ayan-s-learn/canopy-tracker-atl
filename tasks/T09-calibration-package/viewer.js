'use strict';

const $ = id => document.getElementById(id);
const assignment = ASSIGNMENT;
const allowedLayers = Object.keys(assignment.blank.cases[0]?.masks ?? {});
const adjudicating = assignment.blank.role === 'adjudicator';
const ns = 'http://www.w3.org/2000/svg';
const colors = {
  crown_2023: '#8dff9c', unknown_2023: '#fce075', crown_2025: '#8dff9c',
  unknown_2025: '#fce075', unknown_change: '#fce075', loss: '#ff968a',
};
const changeLayers = new Set(['loss', 'unknown_change']);
let response = structuredClone(assignment.blank);
let index = 0;
let draft = [];
let panels = [];

function addElement(parent, name, attributes) {
  const node = document.createElementNS(ns, name);
  for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, value);
  parent.append(node);
  return node;
}

function trace(svg, points, color, closed, dashed = false) {
  addElement(svg, closed ? 'polygon' : 'polyline', {
    points: points.map(([x, y]) => `${x},${y}`).join(' '),
    stroke: color, fill: closed ? color : 'none', 'fill-opacity': dashed ? 0.05 : 0.19,
    'stroke-width': 1.6, 'stroke-dasharray': dashed ? '4 3' : 'none',
    'vector-effect': 'non-scaling-stroke', 'pointer-events': 'none',
  });
}

function repaint() {
  const item = assignment.cases[index];
  const layer = $('layer').value;
  const record = response.cases[index];
  const comparison = $('comparison').value;
  const original = comparison === '' ? null : assignment.originals?.[item.id]?.[Number(comparison)];
  const notes = [];
  if (adjudicating) notes.push(`Review flags: ${assignment.flags[item.id].join(', ')}.`);
  if (original) {
    const time = original.active_minutes === null ? 'Time missing.' : `${original.active_minutes} active min.`;
    const confidence = original.confidence ? `Confidence: ${original.confidence}.` : '';
    const cutoff = original.crop_cutoff ? 'Reader flagged continuation past the crop.' : '';
    notes.push([`Original read: ${original.status}.`, time, confidence, cutoff, original.reason].filter(Boolean).join(' '));
  }
  $('comparison-notes').hidden = !notes.length;
  $('comparison-notes').textContent = notes.join(' ');
  const [x0, y0, x1, y1] = item.core;
  for (const {svg, img, year, mode} of panels) {
    svg.replaceChildren();
    const active = changeLayers.has(layer) ? year === '2023' : layer.endsWith(year);
    svg.classList.toggle('draw', active);
    svg.setAttribute('viewBox', `0 0 ${item.size} ${item.size}`);
    svg.style.width = $('detail').checked ? '150%' : '100%';
    addElement(svg, 'image', {href: img, width: item.size, height: item.size});
    if ($('guide').checked) {
      addElement(svg, 'rect', {x: x0, y: y0, width: x1 - x0, height: y1 - y0, fill: 'none',
        stroke: '#fff', 'stroke-dasharray': '4 3', 'vector-effect': 'non-scaling-stroke'});
      const barX = item.size - 43;
      const barY = item.size - 9;
      addElement(svg, 'rect', {x: barX - 4, y: barY - 11, width: 42, height: 16, fill: '#142720'});
      addElement(svg, 'line', {x1: barX, x2: barX + 20 / assignment.scale_m, y1: barY, y2: barY, stroke: '#fff'});
      addElement(svg, 'text', {x: barX + 7, y: barY - 3, fill: '#fff', 'font-size': 7}).textContent = '20 m';
    }
    for (const mask of allowedLayers.filter(key => key.endsWith(year) || changeLayers.has(key))) {
      if (mask === layer) {
        for (const points of original?.masks[mask] ?? []) trace(svg, points, '#7be7ff', true, true);
      }
      if ($('traces').checked) {
        for (const points of record.masks[mask]) trace(svg, points, colors[mask], true);
      }
    }
    if (active && draft.length) {
      trace(svg, draft, colors[layer], false);
      for (const [x, y] of draft) addElement(svg, 'circle', {cx: x, cy: y, r: 1, fill: colors[layer]});
    }
    svg.setAttribute('aria-label', `${year} ${mode} view of ${item.id}`);
  }
  $('finish').disabled = draft.length < 3;
  $('undo').disabled = !draft.length;
  $('clear').disabled = !draft.length;
  $('polygons').replaceChildren();
  response.cases[index].masks[layer].forEach((_, polygon) => {
    const button = document.createElement('button');
    button.className = 'remove';
    button.textContent = `Remove ${$('layer').selectedOptions[0].textContent} polygon ${polygon + 1}`;
    button.onclick = () => {
      record.masks[layer].splice(polygon, 1);
      repaint();
    };
    $('polygons').append(button);
  });
}

function showCase() {
  const item = assignment.cases[index];
  const current = response.cases[index];
  $('status').value = current.status;
  $('confidence').value = current.confidence ?? '';
  $('cutoff').checked = current.crop_cutoff;
  $('minutes').value = current.active_minutes ?? '';
  $('reason').value = current.reason;
  $('resolution').value = current.resolution ?? '';
  $('case').value = index;
  $('progress').textContent = `Case ${index + 1} of ${assignment.cases.length}`;
  const margin = (item.core[0] * assignment.scale_m).toFixed(1);
  $('registration').textContent = `120 m scoring square, ${margin} m of context per side. ${item.registration}`;
  $('views').replaceChildren();
  panels = [];
  // Each date occupies one column so the two dates can be compared in either band view.
  for (const mode of ['RGB', 'NIR']) {
    item.dates.forEach((date, dateIndex) => {
      const year = ['2023', '2025'][dateIndex];
      const figure = document.createElement('figure');
      const caption = document.createElement('figcaption');
      caption.textContent = `${date} • ${mode === 'NIR' ? 'Near-infrared composite' : 'RGB'}`;
      figure.append(caption);
      const frame = document.createElement('div');
      frame.style.overflow = 'auto';
      frame.addEventListener('scroll', () => {
        for (const {svg} of panels) {
          const other = svg.parentElement;
          if (other !== frame) other.scrollTo(frame.scrollLeft, frame.scrollTop);
        }
      });
      figure.append(frame);
      const svg = addElement(frame, 'svg', {role: 'img'});
      const img = `${item.id}-${year}-${mode.toLowerCase()}.png`;
      svg.addEventListener('click', event => {
        if (!svg.classList.contains('draw')) return;
        const point = new DOMPoint(event.clientX, event.clientY).matrixTransform(svg.getScreenCTM().inverse());
        const snap = value => Math.max(0, Math.min(item.size, Math.round(value)));
        const vertex = [snap(point.x), snap(point.y)];
        if (draft.at(-1)?.every((value, axis) => value === vertex[axis])) return;
        draft.push(vertex);
        if (!$('traces').checked) $('traces').checked = true;
        repaint();
      });
      $('views').append(figure);
      panels.push({svg, img, year, mode});
    });
  }
  repaint();
}

function setNotice(message) {
  $('notice').textContent = message;
}

function setRecord() {
  Object.assign(response.cases[index], {
    status: $('status').value, confidence: $('confidence').value || null,
    crop_cutoff: $('cutoff').checked, active_minutes: $('minutes').value === '' ? null : $('minutes').valueAsNumber,
    reason: $('reason').value.trim(),
  });
  if (adjudicating) response.cases[index].resolution = $('resolution').value || null;
}

function checkRecord(record) {
  if (record.status === 'pending') return 'Choose Read complete, Unreadable or Skipped.';
  if (record.active_minutes !== null && (!Number.isFinite(record.active_minutes) || record.active_minutes < 0)) {
    return 'Enter zero or positive active minutes.';
  }
  const traced = Object.values(record.masks).some(polygons => polygons.length);
  if (record.status !== 'complete' && (traced || record.confidence !== null || record.crop_cutoff)) {
    return 'Remove traces, confidence and the crop flag from a skipped or unreadable case.';
  }
  if (record.status === 'complete' && (record.confidence === null || record.active_minutes === null)) {
    return 'Enter confidence and active minutes for a completed case.';
  }
  const unknown = ['unknown_2023', 'unknown_2025', 'unknown_change'].some(layer => record.masks[layer].length);
  if ((record.status === 'unreadable' || record.crop_cutoff || unknown) && !record.reason) {
    return 'Describe the unreadable image, unknown areas or cropped trace in Reasons.';
  }
  if (record.status === 'unreadable' && record.active_minutes === null) return 'Enter active minutes.';
  if (adjudicating && (!record.resolution || !record.reason || record.active_minutes === null)) {
    return 'Record the adjudication, rationale and active minutes.';
  }
  if (adjudicating && record.resolution === 'resolved' && record.status !== 'complete') {
    return 'A resolved decision needs a completed reading.';
  }
  return '';
}

$('case').onchange = () => {
  if (draft.length) {
    setNotice('Finish or cancel the polygon before changing cases.');
    $('case').value = index;
    return;
  }
  index = Number($('case').value);
  setNotice('');
  showCase();
};
$('layer').onchange = () => {
  if (draft.length) {
    $('layer').value = $('layer').dataset.previous;
    setNotice('Finish or cancel the polygon before changing layers.');
    return;
  }
  $('layer').dataset.previous = $('layer').value;
  setNotice('');
  repaint();
};
for (const field of ['status', 'confidence', 'cutoff', 'minutes', 'reason', 'resolution']) {
  $(field).addEventListener('input', setRecord);
}
for (const field of ['comparison', 'guide', 'traces', 'detail']) $(field).onchange = repaint;

function cross([ax, ay], [bx, by], [cx, cy]) {
  return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax);
}

function onSegment(a, b, point) {
  return point.every((value, i) => value >= Math.min(a[i], b[i]) && value <= Math.max(a[i], b[i]));
}

function intersects(a, b, c, d) {
  const turns = [cross(a, b, c), cross(a, b, d), cross(c, d, a), cross(c, d, b)];
  return (turns[0] * turns[1] < 0 && turns[2] * turns[3] < 0)
    || (turns[0] === 0 && onSegment(a, b, c)) || (turns[1] === 0 && onSegment(a, b, d))
    || (turns[2] === 0 && onSegment(c, d, a)) || (turns[3] === 0 && onSegment(c, d, b));
}

function simplePolygon(points) {
  const count = points.length;
  if (new Set(points.map(point => point.join(','))).size !== count) return false;
  for (const [i, a] of points.entries()) {
    const b = points[(i + 1) % count];
    const c = points[(i + 2) % count];
    if (cross(a, b, c) === 0 && (onSegment(a, b, c) || onSegment(b, c, a))) return false;
    for (let j = i + 2; j < count; j++) {
      if (i === 0 && j === count - 1) continue;
      if (intersects(a, b, points[j], points[(j + 1) % count])) return false;
    }
  }
  return true;
}

$('finish').onclick = () => {
  if (!simplePolygon(draft)) {
    setNotice('Draw a single outline without repeated vertices, overlaps or crossings.');
    return;
  }
  response.cases[index].masks[$('layer').value].push(draft);
  draft = [];
  setNotice('');
  repaint();
};
$('undo').onclick = () => { draft.pop(); repaint(); };
$('clear').onclick = () => { draft = []; setNotice(''); repaint(); };

function download(check) {
  if (draft.length) return setNotice('Finish or cancel the polygon before downloading.');
  const code = $('code').value.trim().toUpperCase();
  const codes = adjudicating ? ['A01'] : ['R01', 'R02'];
  if (!codes.includes(code)) return setNotice(`Enter the assigned code (${codes.join(' or ')}).`);
  response.code = code;
  if (check) {
    for (const record of response.cases) {
      const problem = checkRecord(record);
      if (problem) return setNotice(`${record.id}. ${problem}`);
    }
  }
  const url = URL.createObjectURL(new Blob([JSON.stringify(response, null, 2) + '\n'], {type: 'application/json'}));
  const link = document.createElement('a');
  link.href = url;
  link.download = `canopy-${code}${check ? '' : '-draft'}.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  setNotice('Download requested. Check your browser’s Downloads folder.');
}

$('save').onclick = () => download(true);
$('draft-file').onclick = () => download(false);

$('file').onchange = async event => {
  const [file] = event.target.files;
  event.target.value = '';
  if (!file) return;
  if (draft.length) return setNotice('Finish or cancel the polygon before resuming.');
  try {
    const saved = JSON.parse(await file.text());
    const ids = assignment.cases.map(item => item.id);
    if (saved.packet !== assignment.packet || saved.role !== response.role || !Array.isArray(saved.cases)
        || saved.cases.length !== ids.length || saved.cases.some((record, i) =>
          record.id !== ids[i] || allowedLayers.some(layer => !Array.isArray(record.masks?.[layer])))) {
      throw new Error('This file does not match the assignment.');
    }
    response = saved;
    $('code').value = saved.code;
    showCase();
    setNotice('Saved return loaded.');
  } catch {
    setNotice('Cannot open that return for this assignment.');
  }
};

for (const [position, item] of assignment.cases.entries()) {
  $('case').add(new Option(item.id, position));
}
$('layer').dataset.previous = $('layer').value;
$('comparison-control').hidden = !adjudicating;
$('resolution-control').hidden = !adjudicating;
if (assignment.cases.length) {
  showCase();
} else {
  document.querySelector('main').textContent = 'There are no disagreements requiring adjudication.';
}
