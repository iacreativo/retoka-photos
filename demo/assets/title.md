<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
  <div style="display: flex; align-items: center; gap: 16px;">
    <img src="file/assets/retoka_logo.png" alt="Retoka" style="width: 80px; height: 80px; filter: drop-shadow(0 0 20px rgba(37, 99, 235, 0.4));" onerror="this.src='https://raw.githubusercontent.com/Zeyi-Lin/HivisionIDPhotos/master/assets/hivision_logo.png'; this.onerror=null;">
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
      <b style="font-size: 42px; background: linear-gradient(135deg, #2563eb 0%, #06b6d4 50%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; letter-spacing: -1px; line-height: 1;">Retoka</b>
      <span style="font-size: 14px; color: #06b6d4; margin-top: 2px; font-weight: 500; letter-spacing: 2px;">AI PHOTO EDITING SERVICE</span>
    </div>
  </div>
  <div style="margin-top: 12px; font-size: 18px; color: #2563eb; font-weight: 500;">
    📸 Fotos de identificación para documentos mexicanos
  </div>
  <div style="margin-top: 8px; font-size: 13px; color: #64748b;">
    Powered by AI · Detección facial automática · Tamaño exacto por documento · Listo para imprimir 4x6
  </div>
</div>

<script>
(function() {
    function applySelection() {
        document.querySelectorAll('.checkbox-container').forEach(function(c) {
            var input = c.querySelector('input[type="radio"], input[type="checkbox"]');
            if (input && input.checked) {
                c.classList.add('retoka-selected');
            } else {
                c.classList.remove('retoka-selected');
            }
        });
    }
    setInterval(applySelection, 200);
    document.addEventListener('change', applySelection, true);
    document.addEventListener('click', function(e) {
        setTimeout(applySelection, 50);
    }, true);
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applySelection);
    } else {
        applySelection();
    }
})();
</script>

<style>
.checkbox-container.retoka-selected {
    background: #f3f4f6 !important;
    border-radius: 6px !important;
    padding: 4px 8px !important;
    outline: 2px solid #000000 !important;
}
.checkbox-container.retoka-selected .label-text {
    color: #000000 !important;
    font-weight: 800 !important;
}
.checkbox-container.retoka-selected input {
    background-color: #000000 !important;
    border-color: #000000 !important;
    accent-color: #000000 !important;
}
</style>
