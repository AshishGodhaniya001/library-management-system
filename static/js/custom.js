// helper to show small toast (optional)
function showToast(text, type='info'){
    const wrapper = document.createElement('div');
    wrapper.className = `toast align-items-center text-bg-${type} border-0`;
    wrapper.style.position='fixed';
    wrapper.style.right='20px';
    wrapper.style.bottom='20px';
    wrapper.style.zIndex=9999;
    wrapper.innerHTML = `<div class="d-flex"><div class="toast-body">${text}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>`;
    document.body.appendChild(wrapper);
    const t = new bootstrap.Toast(wrapper);
    t.show();
    setTimeout(()=> t.hide(), 3000);
}
