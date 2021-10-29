let startup = () => {
    let tID = setTimeout(function () {
        let st = document.getElementsByClassName('startup')
        for (var i = 0; i < st.length; i++) {
            st[i].style.visibility = 'visible';
        }
        //window.location.href = "/landing";
        //window.clearTimeout(tID);		// clear time out.
    }, 3000); // timeout 3 secs
    let t2 = setTimeout(function (){
        let bt = document.getElementById('SurfTheOWL_start')
        bt.style.visibility = 'visible';
        let ld = document.getElementById('loader')
        ld.style.visibility = 'hidden';
        let ms = document.getElementById('loading_text')
        let ms_string = ms.innerText
        ms.innerText =ms_string.replace('Loading Ontology:', 'Ontology loaded:')
    }, 4000) // timeout 4 secs
}
window.onload = startup() // if page is loaded call timeout and open main page "/landing"