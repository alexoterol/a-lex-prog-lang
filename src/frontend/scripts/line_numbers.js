const codeInput = document.getElementById('code_input');
const lineNumbers = document.getElementById('line-numbers');

function updateLineNumbers() {
    const text = codeInput.value;
    const lines = text === '' ? 1 : text.split('\n').length;

    let lineNumberText = '';
    for (let i = 1; i <= lines; i++) {
        lineNumberText += i + '\n';
    }

    lineNumbers.textContent = lineNumberText;
}

updateLineNumbers();

codeInput.addEventListener('input', updateLineNumbers);

codeInput.addEventListener('keyup', updateLineNumbers);

codeInput.addEventListener('scroll', () => {
    lineNumbers.scrollTop = codeInput.scrollTop;
});
