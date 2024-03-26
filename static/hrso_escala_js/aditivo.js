function criarContainerlLotesAditivados(LotesAditivados, editavel, idAditivo, aditivoQuantidade) {
    console.log("Aditivo Quantidade: ", aditivoQuantidade)
    let container = document.createElement('div');
    container.classList.add('container-fluid');
    container.setAttribute('id', 'container-lotes-aditivados');

    if(editavel){
        let linhaAcoes = document.createElement('div');
        linhaAcoes.setAttribute('class', 'row');

        let colunaAcoes = document.createElement('div');
        colunaAcoes.setAttribute('class', 'col-12');
        //alinhar a direita
        colunaAcoes.style.textAlign = 'right';
        let botaoAdicionar = document.createElement('div');
        botaoAdicionar.setAttribute('class', 'btn btn-primary');
        botaoAdicionar.setAttribute('onclick', `adicionarLoteAditivo(${idAditivo})`);
        botaoAdicionar.innerHTML = 'Adicionar Lote ao Aditivo';
        botaoAdicionar.style.marginRight = "10px"

        let botaoCancelarAditivo = document.createElement('div');
        botaoCancelarAditivo.setAttribute('class', 'btn btn-danger');
        botaoCancelarAditivo.setAttribute('onclick', `cancelarAditivo(${idAditivo})`);
        botaoCancelarAditivo.innerHTML = 'Cancelar Aditivo';
        botaoCancelarAditivo.style.marginRight = "10px"

        let botaoFinalizarEdicaoAditivo = document.createElement('div');
        botaoFinalizarEdicaoAditivo.setAttribute('class', 'btn btn-success');
        botaoFinalizarEdicaoAditivo.setAttribute('onclick', `FinalizarEdicaoAditivo(${idAditivo})`);
        botaoFinalizarEdicaoAditivo.innerHTML = 'Finalizar Edição';
        botaoFinalizarEdicaoAditivo.style.marginRight = "10px"


        colunaAcoes.appendChild(botaoAdicionar);
        colunaAcoes.appendChild(botaoCancelarAditivo);
        colunaAcoes.appendChild(botaoFinalizarEdicaoAditivo);

        linhaAcoes.appendChild(colunaAcoes);
        container.appendChild(linhaAcoes);
    }
    for(let loteAditivado of LotesAditivados){
        container.append(criarLinhaLoteAditivado(loteAditivado, editavel, idAditivo, aditivoQuantidade));
    }

    return container;
}

function criarLinhaLoteAditivado(loteAditivado, editavel, idAditivo, aditivoQuantidade) {
    let linhaLote = document.createElement('div')
    linhaLote.setAttribute('class', 'row')
    linhaLote.style.paddingTop = "1rem"
    linhaLote.style.paddingBottom = "1rem"
    linhaLote.setAttribute('id', `linhaLoteAditivado-${loteAditivado['id']}`)
    linhaLote.setAttribute('data-numeroLote', `${loteAditivado['numero_lote']}`)

    let colunaConteudoLote = document.createElement('div')
    colunaConteudoLote.setAttribute('class', 'col')

    let linhaDadosLote = document.createElement('div')
    linhaDadosLote.setAttribute('class', 'row')

    let linhaItensLote = document.createElement('div')
    linhaItensLote.setAttribute('class', 'row')

    let coluna1DadosLote = document.createElement('div')
    coluna1DadosLote.setAttribute('class', 'col-8')
    let coluna2DadosLote = document.createElement('div')
    coluna2DadosLote.setAttribute('class', 'col-2')

    let coluna3DadosLote = document.createElement('div')
    coluna3DadosLote.setAttribute('class', 'col-2')

    // verificar se status do contrarto é cadastro
    if(editavel){

        let iconeExcluir = document.createElement('i')
        iconeExcluir.setAttribute('class', 'fas fa-trash-alt')
        iconeExcluir.style.cursor = 'pointer'
        iconeExcluir.setAttribute('onclick', `excluirLoteAditivado(${loteAditivado['id']})`)
        coluna3DadosLote.appendChild(iconeExcluir)
        // alinhar iconeExcluir á direita
        coluna3DadosLote.style.textAlign = "right"
    }
    let conteudoColuna1DadosLote = document.createElement('strong')
    conteudoColuna1DadosLote.appendChild(document.createTextNode(`Lote ${loteAditivado['numero_lote']} - ${loteAditivado['descricao_lote']}`))

    let tabelaItensLoteContrato = criarTabelaItensLoteAditivado(
        loteAditivado['itens_aditivados'],
        loteAditivado['itens_aditivaveis'],
        loteAditivado['id'],
        loteAditivado['numero_lote'],
        editavel,
        idAditivo,
        aditivoQuantidade)
    coluna1DadosLote.appendChild(conteudoColuna1DadosLote)

    linhaItensLote.appendChild(tabelaItensLoteContrato)


    linhaDadosLote.appendChild(coluna1DadosLote)
    linhaDadosLote.appendChild(coluna2DadosLote)
    linhaDadosLote.appendChild(coluna3DadosLote)
    colunaConteudoLote.appendChild(linhaDadosLote)
    colunaConteudoLote.appendChild(linhaItensLote)

    linhaLote.appendChild(colunaConteudoLote)

    return linhaLote;

}
function criarLinhaTabelaItensAditivados(vinculado, item, editavel, idAditivo, aditivoQuantidade, idLote){
    console.log('vinculado ', vinculado)
    console.log("AQ2: ", aditivoQuantidade)
    let linhaItemTabela = document.createElement('tr')

    if(vinculado){
        linhaItemTabela.id = `linhaItemAditivoTabelaVinculado-${item.id_item_lote_licitacao}`
        let td1 = document.createElement('td')
        td1.appendChild(document.createTextNode(`${item.str_numero_item}`))

        let td2 = document.createElement('td')
        td2.appendChild(document.createTextNode(`${item.descricao_item}`))
        let td3 = document.createElement('td')
        td3.appendChild(document.createTextNode(`${item.unidade_medida}`))
        let td4 = document.createElement('td')

        if(aditivoQuantidade){
            if(aditivoQuantidade.editavel){
            elQuantidade = criarInputQuantidadeAditivada(item.id, item.quantidade_contratada, null)
        }else{
                elQuantidade =  document.createTextNode(`${item.quantidade_contratada}`)
        }}else{elQuantidade =  document.createTextNode(`${item.quantidade_contratada}`)}

        td4.appendChild(elQuantidade)
        let td5 = document.createElement('td')
        td5.setAttribute(`data-valorUnitarioItem`, item.valor_item)
        td5.setAttribute(`data-idValorUnitarioItem`, item.id)
        td5.appendChild(document.createTextNode(`${item.valor_item.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))

        let td6 = document.createElement('td')
        let valorTotal = item.quantidade_contratada * item.valor_item
        td6.appendChild(document.createTextNode(`${valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))
        td6.setAttribute('id', 'tdValorTotalItem')
        td6.setAttribute(`data-valorTotalItem`, valorTotal)
        td6.setAttribute(`data-idValorTotalItem`, item.id)
        td6.setAttribute(`data-idLoteValorTotalItem`, idLote)

        let td7 = document.createElement('td')

        if(editavel){
            let iconeExcluir = document.createElement('i')
            iconeExcluir.setAttribute('class', 'fas fa-trash-alt')
            iconeExcluir.style.cursor = "pointer"
            iconeExcluir.style.color = "red"
            iconeExcluir.setAttribute('onclick', `excluirItemLoteAditivo(${item.id})`)
            td7.appendChild(iconeExcluir)
        }else if(aditivoQuantidade){if(aditivoQuantidade.editavel){
            let iconeAtualizarQuantidade = criarIconeAtualizarQuantidade(
                item.id, aditivoQuantidade.id, null)
            td7.appendChild(iconeAtualizarQuantidade)}}

        let td8 = document.createElement('td')
        td8.appendChild(document.createTextNode(`${item.valor_total_faturado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))

        td8.setAttribute('id', 'tdValorFaturadoItem')
        td8.setAttribute(`data-ValorFaturadoItem`, item.valor_total_faturado)

        let saldo = valorTotal - item.valor_total_faturado

        let td9 = document.createElement('td')
        td9.appendChild(document.createTextNode(`${saldo.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))

        linhaItemTabela.appendChild(td1)
        linhaItemTabela.appendChild(td2)
        linhaItemTabela.appendChild(td3)
        linhaItemTabela.appendChild(td4)
        linhaItemTabela.appendChild(td5)
        linhaItemTabela.appendChild(td6)
        linhaItemTabela.appendChild(td7)

        if(!editavel){
            if(aditivoQuantidade){if(!aditivoQuantidade.editavel){
                adicionarTotalFaturadoLinhaTabela(linhaItemTabela, item.valor_item, item.quantidade_contratada,
                        item.valor_total_faturado)}}else{
                 adicionarTotalFaturadoLinhaTabela(linhaItemTabela, item.valor_item, item.quantidade_contratada,
                        item.valor_total_faturado)
            }
        }

    }else{
        linhaItemTabela.setAttribute('id', `linhaItemAditivoTabelaVinculavel-${item.id_item_lote_licitacao}`)
        let td1 = document.createElement('td')
        td1.appendChild(document.createTextNode(`${item.str_numero_item}`))

        let td2 = document.createElement('td')
        td2.appendChild(document.createTextNode(`${item.descricao_item}`))
        let td3 = document.createElement('td')
        td3.appendChild(document.createTextNode(`${item.unidade_medida}`))
        let td4 = document.createElement('td')
        let inputQuantidade = document.createElement('input')
        inputQuantidade.setAttribute('type', 'number')
        inputQuantidade.setAttribute('class', 'form-control')
        inputQuantidade.setAttribute('id', `inputQuantidadeItemLote-${item.id_item_lote_licitacao}`)
        inputQuantidade.setAttribute('onchange', `calcularValorTotalItemLote(${item.id_item_lote_licitacao})`)
        inputQuantidade.setAttribute('value', `${item.quantidade_contratada}`)
        td4.appendChild(inputQuantidade)
        let td5 = document.createElement('td')
        let inputValor = document.createElement('input')
        inputValor.setAttribute('type', 'number')
        inputValor.setAttribute('step', '0.01')
        inputValor.setAttribute('class', 'form-control')
        inputValor.style.minWidth = "6rem"
        inputValor.setAttribute('id', `inputValorItemLote-${item.id_item_lote_licitacao}`)
        inputValor.setAttribute('onchange', `calcularValorTotalItemLote(${item.id_item_lote_licitacao})`)
        inputValor.setAttribute('value', `${item.valor_item}`)
        td5.appendChild(inputValor)
        let td6 = document.createElement('td')
        let inputValorTotal = document.createElement('input')
        inputValorTotal.setAttribute('step', '0.01')
        inputValorTotal.setAttribute('class', 'form-control')
        inputValorTotal.style.minWidth = "9rem"
        inputValorTotal.setAttribute('id', `inputValorTotalItemLote-${item.id_item_lote_licitacao}`)
        inputValorTotal.disabled = true

        let valorTotal = item.valor_item * item.quantidade_contratada
        inputValorTotal.value = valorTotal.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
        td6.appendChild(inputValorTotal)

        let td7 = document.createElement('td')

        let iconeSalvar = document.createElement('i')
        iconeSalvar.setAttribute('class', 'fas fa-plus')
        iconeSalvar.style.cursor = "pointer"
        iconeSalvar.style.color = "green"
        iconeSalvar.setAttribute(
            'onclick',
            `this.removeAttribute('onclick'); salvarItemLoteAditivo(${item.id_item_lote_licitacao}, ${idAditivo})`)
        td7.appendChild(iconeSalvar)

        linhaItemTabela.appendChild(td1)
        linhaItemTabela.appendChild(td2)
        linhaItemTabela.appendChild(td3)
        linhaItemTabela.appendChild(td4)
        linhaItemTabela.appendChild(td5)
        linhaItemTabela.appendChild(td6)
        linhaItemTabela.appendChild(td7)


    }

    return linhaItemTabela
}

function salvarItemLoteAditivo(idItemLoteLicitacao, idAditivo){
    let url = window.location.href
    let dados = criarFormdata("salvar-item-lote-aditivo")

    dados.append('id-aditivo', idAditivo)
    dados.append('id-contrato', id_contrato)
    dados.append("idItemLoteLicitacao", idItemLoteLicitacao)
    dados.append('valor-item-lote', document.getElementById(`inputValorItemLote-${idItemLoteLicitacao}`).value)
    dados.append(
        'quantidade-item-lote', document.getElementById(`inputQuantidadeItemLote-${idItemLoteLicitacao}`
        ).value)

    enviarFormData(dados, processarSalvarItemLoteAditivo)
}

function processarSalvarItemLoteAditivo(response){
    console.log(response)
    if(response.status === 'success'){
        let tabelaAdicionarNovaLinha = document.getElementById(`ItensTabelaLote-${response.idLoteContrato}`)
        let linhaItemTabela = criarLinhaTabelaItensAditivados(true, response.itemContratado, true, response.idAditivo, false,response.idLoteContrato) //(response.itemContratado, response.idLoteContrato)
        let linhaRemover = tabelaAdicionarNovaLinha.querySelector(`#linhaItemAditivoTabelaVinculavel-${response.idItemLoteLicitacao}`)
        tabelaAdicionarNovaLinha.replaceChild(linhaItemTabela, linhaRemover)
    }else{alert(response.errorMessage)}
}

function excluirItemLoteAditivo(idItemLoteAditivo){
    let url = window.location.href
    let dados = criarFormdata("excluir-item-lote-aditivo")

    dados.append('id-item-lote-aditivo-excluir', idItemLoteAditivo)
    dados.append('id-contrato', id_contrato)

    enviarFormData(dados, processarExcluirItemLoteAditivo)

}

function processarExcluirItemLoteAditivo(response){
    console.log(response)
    if(response.status === 'success'){
        let tabelaLinha = document.getElementById(`ItensTabelaLote-${response.idLoteContrato}`)
        console.log(tabelaLinha)
        let linhaItemTabela = criarLinhaTabelaItensAditivados(false, response.itemLicitacao, true, response.idAditivo, null, response.idLoteContrato) //(response.itemContratado, response.idLoteContrato)
        let linhaRemover = tabelaLinha.querySelector(`#linhaItemAditivoTabelaVinculado-${response.itemLicitacao.id_item_lote_licitacao}`)
        tabelaLinha.replaceChild(linhaItemTabela, linhaRemover)
    }else{alert(response.errorMessage)}

}

function excluirLoteAditivado(idLoteAditivo){

    let dados = criarFormdata("excluir-lote-aditivo")
    dados.append('id-lote-aditivo-excluir', idLoteAditivo)
    dados.append('id-contrato', id_contrato)

    enviarFormData(dados, recarregarPagina)

}

function cancelarAditivo(idAditivo){

    let dados = criarFormdata("cancelarAditivo")
    dados.append('id-aditivo', idAditivo)
    dados.append('id-contrato', id_contrato)

    enviarFormData(dados, recarregarPagina)
}

function FinalizarEdicaoAditivo(idAditivo){
    let dados = criarFormdata("FinalizarEdicaoAditivo")
    dados.append('id-aditivo', idAditivo)
    dados.append('id-contrato', id_contrato)

    enviarFormData(dados, recarregarPagina)

}


function criarInputQuantidadeAditivada(idItem, quantidade, idItemProducao){
    let elQuantidade = document.createElement('input')
    elQuantidade.setAttribute('type', 'number')
    elQuantidade.setAttribute('class', 'form-control')
    if(idItemProducao){
        idInput = `inputQuantidadeItemLote-P-${idItemProducao}`
    }else{
       idInput = `inputQuantidadeItemLote-${idItem}`
    }
    elQuantidade.setAttribute('id', idInput)
    elQuantidade.setAttribute('onchange',
        `processarQuantidadeAlteradaAditivoContrato(${idItem}, this, ${idItemProducao})`)
    elQuantidade.setAttribute('value', `${quantidade}`)

    return elQuantidade
}


function criarIconeAtualizarQuantidade(idItem, ididAditivoQuantidade, idItemProducao){
    let iconeAtualizarQuantidade = document.createElement('i')
    iconeAtualizarQuantidade.setAttribute('class', 'fas fa-sync-alt')
    if(idItemProducao){idIcone = `iconeAtualizarQuantidadeItem-P-${idItemProducao}`
        funcaoAditivarQuantidade = `aditivoQuantidadeItemProducaoAtualizar('${idItemProducao}', '${ididAditivoQuantidade}', this)`}else{
        idIcone = `iconeAtualizarQuantidadeItem-${idItem}`
        iconeAtualizarQuantidade.setAttribute('id', idIcone)
        funcaoAditivarQuantidade = `aditivoQuantidadeItemAtualizar('${idItem}', '${ididAditivoQuantidade}', this)`}

    iconeAtualizarQuantidade.setAttribute('onclick', funcaoAditivarQuantidade)
    iconeAtualizarQuantidade.style.color = 'green'
    iconeAtualizarQuantidade.style.cursor = 'pointer'

    return iconeAtualizarQuantidade}

function adicionarLoteAditivo(idAditivo){

    const idModal = 'janela-adicionar-lote-aditivo';

    if(document.getElementById(idModal)){
        let modal = new bootstrap.Modal(document.getElementById(idModal))
        modal.show()
    }else{
        const tituloModal = "Informações do Aditivo:"

        const conteudoModal = criarConteudoModalAdicionarLoteAditivo(idAditivo)

        let janela_modal = criarModal(idModal, tituloModal, conteudoModal)

        document.body.appendChild(janela_modal)
        modal = new bootstrap.Modal(janela_modal)
        modal.show()
    }
}

function criarConteudoModalAdicionarLoteAditivo(idAditivo){

    let containerJanela = document.createElement('div');
    containerJanela.setAttribute('class', 'container-fluid');

    let formulario = criarFormularioBase("adicionarLotesAditivo")

    let input3 = document.createElement('input');
    input3.setAttribute('type', 'hidden');
    input3.setAttribute('name', 'id-contrato');
    input3.setAttribute('value', id_contrato);

    let input4 = document.createElement('input');
    input4.setAttribute('type', 'hidden');
    input4.setAttribute('name', 'id_aditivo');
    input4.setAttribute('value', idAditivo);

    formulario.appendChild(input3);
    formulario.appendChild(input4);

    let lotesAditivaveis = visualizacao.lotes_contrataveis
    for(lote of lotesAditivaveis){
        let linhaLote = document.createElement('div');
        linhaLote.setAttribute('class', 'row');

        let colunaLote = document.createElement('div');
        colunaLote.setAttribute('class', 'col');

        let divLote = document.createElement('div');
        divLote.setAttribute('class', 'container-fluid');


        let labelLote = document.createElement('label');
        labelLote.setAttribute('class', 'form-check-label');
        labelLote.appendChild(document.createTextNode(`Lote ${lote.numero_lote} - ${lote.descricao_lote}`));

        let checkboxLote = document.createElement('input');
        checkboxLote.setAttribute('type', 'checkbox');
        checkboxLote.setAttribute('class', 'form-check-input');
        checkboxLote.setAttribute('name', `id-lotes-aditivados`);
        checkboxLote.setAttribute('value', lote.id);

        divLote.appendChild(checkboxLote);
        divLote.appendChild(labelLote);

        colunaLote.appendChild(divLote);
        linhaLote.appendChild(colunaLote);
        formulario.appendChild(linhaLote);
    }

    let submitForm = document.createElement('button');
    submitForm.setAttribute('type', 'submit');
    submitForm.setAttribute('class', 'btn btn-primary');
    submitForm.appendChild(document.createTextNode('Adicionar lotes'));

    formulario.appendChild(document.createElement('br'));
    formulario.appendChild(submitForm);

    containerJanela.appendChild(formulario);

    return containerJanela
}

function aditivoQuantidadeItemAtualizar(idItem, idAditivoQuantidade, iconeAtualizar){
    let inputQuantidade = document.getElementById(`inputQuantidadeItemLote-${idItem}`)
    let dados = criarFormdata("atualizar-item-aditivo-quantidade")

    dados.append('id-item', idItem)
    dados.append('id-aditivo-quantidade', idAditivoQuantidade)
    dados.append('quantidade-atualizada', inputQuantidade.value)
    dados.append('idIconeAtualizar', iconeAtualizar.id)

    enviarFormData(dados, processarAtualizarItemAditivoQuantidade)
}

function processarAtualizarItemAditivoQuantidade(response){
    iconeAtualizar = document.getElementById(response.idIconeAtualizar)
    if(response.status === 'success'){iconeAtualizar.style.color = "green"}else{alert("Erro ao atualizar o item")}}

function processarQuantidadeAlteradaAditivoContrato(idItemLoteContrato, inputQuantidade, idItemLoteProducao){

    if(idItemLoteContrato){
        console.log("A")
        idIcone = `iconeAtualizarQuantidadeItem-${idItemLoteContrato}`
         tdValorUnitario = document.querySelector(`td[data-idvalorUnitarioItem="${idItemLoteContrato}"]`)
         v = tdValorUnitario.getAttribute('data-valorUnitarioItem')
         tdValorTotal = document.querySelector(`td[data-idValorTotalItem="${idItemLoteContrato}"]`)

    }else{
        console.log("B")
        idIcone = `iconeAtualizarQuantidadeItem-P-${idItemLoteProducao}`
        tdValorUnitario = document.querySelector(`td[data-idvalorUnitarioItemProducao="${idItemLoteProducao}"]`)
        console.log(tdValorUnitario)
        v = tdValorUnitario.getAttribute('data-valorUnitarioItemProducao')
        tdValorTotal = document.querySelector(`td[data-idValorTotalItemLoteProducao="${idItemLoteProducao}"]`)
    }
    let icone = document.getElementById( idIcone)
    icone.style.color = 'red'

    let q = inputQuantidade.value

    let valorTotal = Number(q)*Number(v)

    console.log(v, q, valorTotal)

    tdValorTotal.removeChild(tdValorTotal.firstChild)
    tdValorTotal.appendChild(document.createTextNode(valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })))
    tdValorTotal.setAttribute('data-valorTotalItem', valorTotal)
    let idLote = tdValorTotal.getAttribute('data-idLoteValorTotalItem') // idLoteValorTotalItem
    processarValorTotalLote(idLote)
}

function finalizarAditivoQuantidade(e) {
    let idAditivo = e.getAttribute('data-idaditivoquantidade')

    let dados = criarFormdata("finalizar-aditivo-quantidade")
    dados.append('id-aditivo-quantidade', idAditivo)
    dados.append('id-contrato', id_contrato)

    enviarFormData(dados, recarregarPagina)
}

function cancelarAditivoQuantidade(e) {
    let idAditivo = e.getAttribute('data-idaditivoquantidade')

    let dados = criarFormdata("cancelar-aditivo-quantidade")
    dados.append('id-aditivo-quantidade', idAditivo)
    dados.append('id-contrato', id_contrato)

    enviarFormData(dados, recarregarPagina)
}

