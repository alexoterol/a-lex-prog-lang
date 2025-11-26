const codeInput = document.getElementById('code_input');
const button = document.getElementById('run_button');
const code = codeInput.value

button.addEventListener('click', () => {
    fetch('http://127.0.0.1:8000/get_errors', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ code: codeInput.value })
    })
    .then(res => res.json())
    .then(data => {
        if (data != null) {
            const output_text = document.getElementById('output-text');
            output_text.textContent = data.result
        }
    })
})
