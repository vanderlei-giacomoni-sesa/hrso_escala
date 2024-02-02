
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function criarFormdata(tipoAcao){
    console.log(csrftoken);

    let fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrftoken);
    fd.append('tipo-acao', tipoAcao);

    console.log('FormData', fd);
    return fd
}

function criarFormularioBase(tipoAcao){

    let formulario = document.createElement('form')
    formulario.method = "POST"

    const inputTipoAcao = document.createElement('input')
    inputTipoAcao.hidden = true
    inputTipoAcao.name = "tipo-acao"
    inputTipoAcao.value = tipoAcao

    const inputCsrftoken = document.createElement('input')
    inputCsrftoken.hidden = true
    inputCsrftoken.name = "csrfmiddlewaretoken"
    inputCsrftoken.value = csrftoken

    formulario.appendChild(inputTipoAcao)
    formulario.appendChild(inputCsrftoken)

    return formulario
}

function enviarFormData(formData, callbackFunction) {
    fetch(window.location.href, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => callbackFunction(data))
        .catch(error => console.error(error));
}


window.None = null
window.True = true
window.False = false


window.csrftoken = getCookie('csrftoken');