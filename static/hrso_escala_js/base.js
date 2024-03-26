
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

function ajustarAlturaJanelaLotes(idContainer, alturaDescontar){
    alturaContainerLotes = window.innerHeight - alturaDescontar
    containerLotes = document.getElementById(idContainer)
    containerLotes.style.height = `${alturaContainerLotes}px`
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
    inputTipoAcao.id=`id-${tipoAcao}`
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

function criarModal(idModal, tituloModal, conteudoModal, tamanhoModal){
    let modal = document.createElement('div')
    modal.className = "modal"
    modal.id= idModal

    let modalDialog = document.createElement('div')
    if(tamanhoModal){
        modalDialog.className = `modal-dialog ${tamanhoModal}`
    }else{modalDialog.className = "modal-dialog"}


    let modalContent = document.createElement("div")
    modalContent.className = "modal-content"

    ///////////////////// CAbeçalho do Modal ///////////////////////////
    let modalHeader = document.createElement('div')
    modalHeader.className = "modal-header"

    let modalTitle = document.createElement('H4')
    modalTitle.className = "modal-title"
    modalTitle.appendChild(document.createTextNode(tituloModal))

    let btnCloseModal = document.createElement('button')
    btnCloseModal.type = "button"
    btnCloseModal.className = "btn-close"
    btnCloseModal.setAttribute("data-bs-dismiss", "modal")

    modalHeader.appendChild(modalTitle)
    modalHeader.appendChild(btnCloseModal)
    ///////////////////////////////////////////////////////////////////
    /////////////////  Conteudo do Modal  /////////////////////////////

    let modalBody = document.createElement("div")
    modalBody.className = "modal-body"

    modalBody.appendChild(conteudoModal)

    ///////////////////////////////////////////////////////////////////

    modalContent.appendChild(modalHeader)
    modalContent.appendChild(modalBody)

    modalDialog.appendChild(modalContent)
    modal.appendChild(modalDialog)

    return modal
}

function criarModalSelect(id, option){
    console.log(option)
    console.log(options)
    const titulo = options[option]['titulo']
    const optionKey = options[option]['optionKey']
    const opcoes = options[option]['options']
    const funcaoBuscar = options[option]['funcaoBuscar']

    console.log(titulo, optionKey, opcoes, funcaoBuscar)


    const idModal = `idSelect${option}`

    if(document.getElementById(idModal)){
        let modal = new bootstrap.Modal(document.getElementById(idModal))
        modal.show()
    }else{
        const tituloModal = titulo

        const conteudoModal = criarConteudoModalSelect(id, opcoes, optionKey, funcaoBuscar, option)

        let janela_modal = criarModal(idModal, tituloModal, conteudoModal)

        document.body.appendChild(janela_modal)
        modal = new bootstrap.Modal(janela_modal)
        modal.show()

    }


}


function criarModalInputSelect(id, option){
    console.log(option)
    console.log(options)
    const titulo = options[option]['titulo']
    const optionKey = options[option]['optionKey']
    const opcoes = options[option]['options']
    const funcaoBuscar = options[option]['funcaoBuscar']

    console.log(titulo, optionKey, opcoes, funcaoBuscar)


    const idModal = `idSelect${option}`

    if(document.getElementById(idModal)){
        let modal = new bootstrap.Modal(document.getElementById(idModal))
        modal.show()
    }else{
        const tituloModal = titulo

        const conteudoModal = criarConteudoModalInputSelect(id, opcoes, optionKey, funcaoBuscar, option)

        let janela_modal = criarModal(idModal, tituloModal, conteudoModal)

        document.body.appendChild(janela_modal)
        modal = new bootstrap.Modal(janela_modal)
        modal.show()

    }


}

function criarConteudoModalSelect(id, opcoes, optionKey, funcaoBuscar, option){
    let containerModal = document.createElement('div')
    containerModal.className = "container-fluid"
    containerModal.appendChild(criarSelect(id, opcoes, optionKey, funcaoBuscar, option))


    return containerModal
}


function criarConteudoModalInputSelect(id, opcoes, optionKey, funcaoBuscar, option){
    let containerModal = document.createElement('div')
    containerModal.className = "container-fluid"
    containerModal.appendChild(criarInputSelect(id, opcoes, optionKey, funcaoBuscar, option))


    return containerModal
}


function validarSelect(select) {
    if (select.value !== "") {
        select.classList.remove("is-invalid");
        select.classList.add("is-valid");
    } else {
        select.classList.remove("is-valid");
        select.classList.add("is-invalid");
    }
}


function criarSelect(id, opcoes, optionKey, funcaoBuscar, option) {
    let objetoHTML = document.createElement('div');
    objetoHTML.className = "row";

    let divCol = document.createElement('div');
    divCol.className = "col";

    let h5 = document.createElement('h5');
    h5.appendChild(document.createTextNode("Selecione: "));

    divCol.appendChild(h5);

    let selectFuncoes = document.createElement('select')
    selectFuncoes.className = "form-select"
    selectFuncoes.id = `select-${option}-${id}`
    selectFuncoes.required = true
    selectFuncoes.setAttribute('onchange', "validarSelect(this)")

    let opcao_disabled = document.createElement('option');
    opcao_disabled.disabled = true
    opcao_disabled.text = "escolha uma opção"

    let opcao_blank = document.createElement('option');

    selectFuncoes.appendChild(opcao_disabled);
    selectFuncoes.appendChild(opcao_blank);

    for(let o of opcoes){
        let opcao = document.createElement('option');
        opcao.value = o['id'];
        opcao.text = o[optionKey];
        selectFuncoes.appendChild(opcao);
    }


    let invalidFeedback = document.createElement('div');
    invalidFeedback.className = "invalid-feedback";
    invalidFeedback.textContent = "Por favor, selecione uma opção.";

    let validFeedback = document.createElement('div');
    validFeedback.className = "valid-feedback";
    validFeedback.textContent = "";

    let botaoBuscar = document.createElement('input');
    botaoBuscar.setAttribute('class', 'btn btn-success');
    botaoBuscar.setAttribute('value', 'Selecionar');
    botaoBuscar.setAttribute('onclick', `${funcaoBuscar}(${id}, '${option}')`)

    divCol.appendChild(selectFuncoes)
    divCol.appendChild(document.createElement('br'))
    divCol.appendChild(validFeedback)
    divCol.appendChild(invalidFeedback)
    divCol.appendChild(botaoBuscar)


    objetoHTML.appendChild(divCol);

    return objetoHTML;

}

function criarInputSelect(id, opcoes, optionKey, funcaoBuscar, option) {
    let objetoHTML = document.createElement('div');
    objetoHTML.className = "row";

    let divCol = document.createElement('div');
    divCol.className = "col";

    let h5 = document.createElement('h5');
    h5.appendChild(document.createTextNode("Selecione: "));

    divCol.appendChild(h5);

    let linha1 = document.createElement('div')
    linha1.className = "row";

    let colunaLinha1 = document.createElement('div');
    colunaLinha1.className = 'col'



    let linha2 = document.createElement('div')
    linha2.className = "row";

    let colunaLinha2 = document.createElement('div');
    colunaLinha2.className = 'col'

    let linha3 = document.createElement('div')
    linha3.className = "row";

    let colunaLinha3 = document.createElement('div');
    colunaLinha3.className = 'col'


    var inputSelect = document.createElement('input');
    inputSelect.type = "text"
    inputSelect.className = "form-control"
    inputSelect.id = `input-select-${option}-${id}`
    inputSelect.placeholder = "localizar ou selecionar"
    inputSelect.setAttribute('list', `datalist-${option}-${id}`);
    inputSelect.dataset.optionid = ''; // Adiciona dataset.optionid ao input
    inputSelect.style.width = "100%"

    var datalist = document.createElement('datalist');
    datalist.id = `datalist-${option}-${id}`;
    datalist.style.width = "100%"

    for(let o of opcoes){
        let optionDatalist = document.createElement('option');
        optionDatalist.style.width = "100%"
        optionDatalist.value = o[optionKey];
        optionDatalist.dataset.optionid =  o['id'];
        datalist.appendChild(optionDatalist);
    }

    // Adiciona um ouvinte de eventos para o input
    inputSelect.addEventListener('input', function(event) {
        let value = event.target.value;
        let options = datalist.getElementsByTagName('option');
        for (let option of options) {
            if (option.value === value) {
                // Atualiza o dataset.optionid do input com o valor correspondente da opção selecionada
                inputSelect.dataset.optionid = option.dataset.optionid;
                break;
            }
        }
    });

    let invalidFeedback = document.createElement('div');
    invalidFeedback.className = "invalid-feedback";
    invalidFeedback.textContent = "Por favor, selecione uma opção.";

    let validFeedback = document.createElement('div');
    validFeedback.className = "valid-feedback";
    validFeedback.textContent = "";

    let botaoBuscar = document.createElement('input');
    botaoBuscar.setAttribute('class', 'btn btn-success');
    botaoBuscar.setAttribute('value', 'Selecionar');
    botaoBuscar.setAttribute('onclick', `${funcaoBuscar}(${id}, '${option}')`);

    colunaLinha1.appendChild(inputSelect);
    colunaLinha2.appendChild(datalist); // Adiciona o datalist ao HTML
    colunaLinha1.appendChild(validFeedback);
    colunaLinha1.appendChild(invalidFeedback);
    colunaLinha3.appendChild(document.createElement('br'))
    colunaLinha3.appendChild(botaoBuscar);

    linha1.appendChild(colunaLinha1)
    linha2.appendChild(colunaLinha2)
    linha3.appendChild(colunaLinha3)

    divCol.append(linha1, linha2, linha3)

    objetoHTML.appendChild(divCol);

    return objetoHTML;
}

window.None = null
window.True = true
window.False = false


window.csrftoken = getCookie('csrftoken');