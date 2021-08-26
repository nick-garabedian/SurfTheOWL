function copy_to_clipboard(copy_value) {
    var el = document.createElement('textarea');
    el.value = copy_value;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}