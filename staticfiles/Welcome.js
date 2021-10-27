let redirect_Page = () => {
    let tID = setTimeout(function () {
        window.location.href = "/landing";
        window.clearTimeout(tID);		// clear time out.
    }, 3000); // timeout 3 secs
}
window.onload = redirect_Page() // if page is loaded call timeout and open main page "/landing"