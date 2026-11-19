(() => {
  const input = document.getElementById('resume-file');
  const zone = document.getElementById('drop-zone');
  const label = document.getElementById('file-label');
  const form = document.getElementById('upload-form');
  if (!input || !zone || !label || !form) return;
  const setFile = (file) => {
    if (!file) return;
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx'].includes(ext)) { alert('Choose a PDF or DOCX file.'); input.value = ''; return; }
    if (file.size > 8 * 1024 * 1024) { alert('Choose a file smaller than 8 MB.'); input.value = ''; return; }
    label.textContent = file.name;
    zone.classList.add('has-file');
  };
  input.addEventListener('change', () => setFile(input.files[0]));
  ['dragenter', 'dragover'].forEach(type => zone.addEventListener(type, e => { e.preventDefault(); zone.classList.add('dragging'); }));
  ['dragleave', 'drop'].forEach(type => zone.addEventListener(type, e => { e.preventDefault(); zone.classList.remove('dragging'); }));
  zone.addEventListener('drop', e => { const file = e.dataTransfer.files[0]; if (file) { try { const transfer = new DataTransfer(); transfer.items.add(file); input.files = transfer.files; } catch (_) {} setFile(file); } });
  form.addEventListener('submit', () => { const button = form.querySelector('button[type="submit"]'); button.disabled = true; button.querySelector('span:first-child').textContent = 'Analyzing…'; });
})();
