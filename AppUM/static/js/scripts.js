function showInventarios() {
    document.getElementById('inventarios').style.display = 'block';
}

function toggleMotoForm() {
    const form = document.getElementById('motoForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}