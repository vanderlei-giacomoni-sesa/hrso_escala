function excluirLoteLicitacao(idExcluir){
    let confirmarExclusao = confirm('Confirmar a exclusão?')

    if(confirmarExclusao === true){
        let dados = criarFormdata('excluirLoteLicitacao')
        dados.append('id_lote_licitacao_excluir', idExcluir)
        enviarFormData(dados, processarExcluirLoteLicitacao)
    }
}

function processarExcluirLoteLicitacao(response){
    if(response.status === 'success'){
        let linhaExcluir = document.getElementById('linhaLoteLicitacao-'.concat(response.id_lote_licitacao_excluir))
        linhaExcluir.remove()
    }else if(response.status === 'error'){
        console.log(response.error)
        alert(response.error)
    }
}

function tabelaLotesLicitacao(lotesLicitacao){
    let containerTabela = document.getElementById('container-tabela-lotes')
    for(let lote of lotesLicitacao){
        console.log(lote)
        let linhaLoteLicitacao = criarLinhaLote(lote)
        containerTabela.appendChild(linhaLoteLicitacao)
        atualizarValorTotalLote(lote['id'])
    }
}

function adicionarLinhaInputItemLote(numeroProximoItem, idLote) {
    let tabelaLote = document.getElementById(`ItensTabelaLote-${idLote}`)
    let linhaInputItemLote = criarLinhaInputItemLote(idLote, numeroProximoItem)
    tabelaLote.appendChild(linhaInputItemLote)

}

function adicionarItemLote(idLote){

    let li = []
    // uma lista com os valores dos data-atrtributes no formato `data-itemLinhaLote-${idLote}'
    document.querySelectorAll(`[data-itemLinhaLote-${idLote}]`).forEach(function (item) {
        li.push(item.getAttribute('data-itemLinhaLote-' + idLote))
    })
    let npi = numeroProximoItem(li)

    adicionarLinhaInputItemLote(npi, idLote)

}


function excluirItemLoteLicitacao(idItemLoteExcluir){

    let confirmarExclusao = confirm('Confirmar a exclusão?')

    if(confirmarExclusao === true){
        let dados = criarFormdata("excluirItemLoteLicitacao")

        dados.append('idItemLoteExcluir', idItemLoteExcluir)

        enviarFormData(dados, processarExcluirItemLicitacao)
    }
}


function processarExcluirItemLicitacao(response){
    if(response.status === 'success'){
        let linhaExcluir = document.getElementById(`linhaItemLoteLicitacao-${response.idItemLoteExcluir}`)
        linhaExcluir.remove()
        atualizarValorTotalLote(response.idLoteExcluido)
    }else{console.log(response.error)}
}

function criarLinhaItemLote(itemLote, idLote){
    console.log("IL", itemLote)
    let linhaLote = document.createElement('tr')
    linhaLote.setAttribute('id', `linhaItemLoteLicitacao-${itemLote['id']}`)
    linhaLote.setAttribute(`data-itemLinhaLote-${idLote}`, itemLote['numero_item'])

    let td0 = document.createElement('td')

    let iconeExcluirItemLote = document.createElement('i')
    iconeExcluirItemLote.setAttribute('class', 'fas fa-times')
    iconeExcluirItemLote.style.color = 'red'
    iconeExcluirItemLote.style.cursor = "pointer"
    iconeExcluirItemLote.setAttribute('onclick', `excluirItemLoteLicitacao('${itemLote['id']}')`)
    if(!edicaoFinalizada){
        td0.appendChild(iconeExcluirItemLote)
    }

    let td1 = document.createElement('td')
    td1.appendChild(document.createTextNode(itemLote['str_numero_item']))
    let td2 = document.createElement('td')
    td2.appendChild(document.createTextNode(itemLote['descricao_item']))
    let td3 = document.createElement('td')
    td3.appendChild(document.createTextNode(itemLote['unidade_medida']))
    let td4 = document.createElement('td')
    td4.appendChild(document.createTextNode(itemLote['quantidade_licitada']))
    let td5 = document.createElement('td')
    td5.appendChild(document.createTextNode(Number(itemLote['valor_licitado']).toLocaleString('pt-BR', {minimumFractionDigits: 2 , style: 'currency', currency: 'BRL' })))
    let td6 = document.createElement('td')
    let valor_item = itemLote['quantidade_licitada']*itemLote['valor_licitado']
    td6.appendChild(document.createTextNode(valor_item.toLocaleString('pt-BR', {minimumFractionDigits: 2 , style: 'currency', currency: 'BRL' })))
    td6.setAttribute('id', `valorTotalItemLote-${itemLote['id']}`)
    td6.setAttribute(`data-valorTotalItemLote-${idLote}`, valor_item)

    linhaLote.appendChild(td0)
    linhaLote.appendChild(td1)
    linhaLote.appendChild(td2)
    linhaLote.appendChild(td3)
    linhaLote.appendChild(td4)
    linhaLote.appendChild(td5)
    linhaLote.appendChild(td6)

    return linhaLote

}

function salvarItemLoteLicitacao(idLote, numeroItemLote){
    let numeroItemEnviar = document.getElementById(`inputNumeroItemLote-${idLote}-${numeroItemLote}`).value
    let unidadeMedida = document.getElementById(`idInputUnLote-${idLote}-${numeroItemLote}`).value
    let descricaoSalvar = document.getElementById(`inputDescricaoItemLote-${idLote}-${numeroItemLote}`).value
    let quantidadeSalvar = document.getElementById(`inputQuantidadeItemLote-${idLote}-${numeroItemLote}`).dataset.quantidade
    let valorSalvar = document.getElementById(`inputValorItemLote-${idLote}-${numeroItemLote}`).value

    if(validarDadosInputItemLote(idLote, numeroItemLote)){
        console.log("Ok, até aqui")
        let dados = criarFormdata("adicionarItemLoteLicitacao")

        dados.append('id_lote_licitacao_alterar', idLote)
        dados.append('numero_item', numeroItemEnviar)
        dados.append('numeroItemLote', numeroItemLote)
        dados.append('unidadeMedida', unidadeMedida)
        dados.append('descricao_item_salvar', descricaoSalvar)
        dados.append('quantidade_licitada_salvar', quantidadeSalvar)
        dados.append('valor_licitado_salvar', valorSalvar)


        enviarFormData(dados, processarItemLoteLicitacaoAdicionado)

    }else{
        if(!numeroItemEnviar){
            document.getElementById(`inputNumeroItemLote-${idLote}-${numeroItemLote}`).classList.add('is-invalid')
        }
        if(!unSalvar){
            document.getElementById(`idInputUnLote-${idLote}-${numeroItemLote}`).classList.add('is-invalid')
        }
        if(!descricaoSalvar){
            document.getElementById(`inputDescricaoItemLote-${idLote}-${numeroItemLote}`).classList.add('is-invalid')
        }
        if(!quantidadeSalvar){
            document.getElementById(`inputQuantidadeItemLote-${idLote}-${numeroItemLote}`).classList.add('is-invalid')
        }
        if(!valorSalvar){
            document.getElementById(`inputValorItemLote-${idLote}-${numeroItemLote}`).classList.add('is-invalid')
        }

    }}

function processarItemLoteLicitacaoAdicionado(response){
    console.log("processarItemLoteLicitacaoAdicionado: ", response)
    let idLote = response.idLote
    let numeroItemLote = response.numeroItemLote
    let numeroItemLoteLinha = response.numeroItemLoteLinha

    if(response.status === 'success'){

        let itemSalvo = response.item_salvo

        let loteSelecionado = lotesLicitacao.find(obj=> obj.id==idLote)
        let indexLote = lotesLicitacao.indexOf(loteSelecionado)
        document.getElementById(`linhaInputLote-${idLote}-${numeroItemLoteLinha}`).remove()
        let linha = criarLinhaItemLote(itemSalvo, idLote)
        let tbodyLote = document.getElementById(`ItensTabelaLote-${idLote}`)

        tbodyLote.append(linha)

        atualizarValorTotalLote(idLote)
        lotesLicitacao[indexLote].itens_lote.push(itemSalvo)

    }else if (response.status === 'erro-item-ja-cadastrado'){
        alert(`Erro ao salvar o item ${numeroItemLote} do Lote ${response.numero_lote}. Já existe um item cadastrado com o numero para esse lote`)
    }
}


function removerClasseInvalido(thisInput){
    if(thisInput.classList.contains('is-invalid')){
        thisInput.classList.remove('is-invalid')
    }
}

function excluirLinhaItemLoteLicitacao(idLote, numeroItemLote){
    document.getElementById(`linhaInputLote-${idLote}-${numeroItemLote}`).remove()
}

function numeroProximoItem(listaItens){
    if (listaItens.length === 0) {return 1}
    const listaItensInt = listaItens.map(Number);
    return Math.max(...listaItensInt) + 1
}

function validarDadosInputItemLote(idLote, numeroItemLote){
    let numeroItem = document.getElementById(`inputNumeroItemLote-${idLote}-${numeroItemLote}`).value
    let un = document.getElementById(`idInputUnLote-${idLote}-${numeroItemLote}`).value
    let descricao = document.getElementById(`inputDescricaoItemLote-${idLote}-${numeroItemLote}`).value
    let quantidade = document.getElementById(`inputQuantidadeItemLote-${idLote}-${numeroItemLote}`).value
    let valor = document.getElementById(`inputValorItemLote-${idLote}-${numeroItemLote}`).value

    return !(numeroItem === '' || un === '' || descricao === '' || quantidade === '' || valor === '');

}

function criarLinhaInputItemLote(idLote, numeroItemLote){

    let idLinhaInputLote = `linhaInputLote-${idLote}-${numeroItemLote}`

    //se já existir uma linha com esse id, não cria novamente
    if(document.getElementById(idLinhaInputLote)) {
        let li = []
        // uma lista com os valores dos data-atrtributes no formato `data-itemLinhaLote-${idLote}'
        document.querySelectorAll(`[data-itemLinhaLote-${idLote}]`).forEach(function (item) {
            li.push(item.getAttribute('data-itemLinhaLote-' + idLote))
        })
        numeroItemLote = numeroProximoItem(li)
        idLinhaInputLote = `linhaInputLote-${idLote}-${numeroItemLote}`
    }

    let linhaLote = document.createElement('tr')
    linhaLote.setAttribute('id', idLinhaInputLote)
    linhaLote.setAttribute(`data-itemLinhaLote-${idLote}`, numeroItemLote)

    let td0 = document.createElement('td')

    let iconeSalvarItemLote = document.createElement('i')
    iconeSalvarItemLote.setAttribute('class', 'fas fa-check')
    iconeSalvarItemLote.style.color = 'green'
    iconeSalvarItemLote.style.cursor = "pointer"
    iconeSalvarItemLote.setAttribute('onclick', `salvarItemLoteLicitacao('${idLote}', '${numeroItemLote}')`)

    let iconeExcluirLinhaItemLote = document.createElement('i')
    iconeExcluirLinhaItemLote.setAttribute('class', 'fas fa-times')
    iconeExcluirLinhaItemLote.style.color = 'red'
    iconeExcluirLinhaItemLote.style.cursor = "pointer"
    iconeExcluirLinhaItemLote.setAttribute('onclick', `excluirLinhaItemLoteLicitacao('${idLote}', '${numeroItemLote}')`)

    td0.appendChild(iconeSalvarItemLote)
    td0.appendChild(document.createElement('br'))
    td0.appendChild(iconeExcluirLinhaItemLote)


    let td1 = document.createElement('td')
    let inputNumeroItem = document.createElement('input')
    inputNumeroItem.setAttribute('class', 'form-control')
    inputNumeroItem.setAttribute('type', 'number')
    inputNumeroItem.setAttribute('min', 1)
    inputNumeroItem.setAttribute('id', `inputNumeroItemLote-${idLote}-${numeroItemLote}`)
    inputNumeroItem.setAttribute('onchange', `removerClasseInvalido(this)`)
    inputNumeroItem.value = numeroItemLote
    td1.appendChild(inputNumeroItem)

    let td2 = document.createElement('td')
    let inputSelectUn = document.createElement('select')
    inputSelectUn.setAttribute('class', 'form-control')
    inputSelectUn.setAttribute('name', 'selectUn')
    inputSelectUn.setAttribute('id', `idInputUnLote-${idLote}-${numeroItemLote}`)
    inputSelectUn.setAttribute('onchange', `removerClasseInvalido(this)`)

    let optionBlank = document.createElement('option')
    optionBlank.setAttribute('value', '')
    optionBlank.innerHTML = 'Selecione'
    optionBlank.disabled = true
    optionBlank.selected = true

    inputSelectUn.appendChild(optionBlank)

    for(let u of window.unidadesMedida){

        let optionUn = document.createElement('option')
        optionUn.setAttribute('value', u[0])
        optionUn.appendChild(document.createTextNode(u[1]))

        inputSelectUn.appendChild(optionUn)
    }


    let td3 = document.createElement('td')
    let inputDescricaoItem = document.createElement('input')
    inputDescricaoItem.setAttribute('class', 'form-control')
    inputDescricaoItem.setAttribute('type', 'text')
    inputDescricaoItem.setAttribute('id', `inputDescricaoItemLote-${idLote}-${numeroItemLote}`)
    inputDescricaoItem.setAttribute('onchange', `removerClasseInvalido(this)`)

    td2.appendChild(inputDescricaoItem)
    td3.appendChild(inputSelectUn)

    let td4 = document.createElement('td')

    let inputQuantidadeItem = document.createElement('input')
    inputQuantidadeItem.setAttribute('class', 'form-control')
    //inputQuantidadeItem.setAttribute('type', 'number')
    inputQuantidadeItem.setAttribute('step', "0.01")
    inputQuantidadeItem.setAttribute('id', `inputQuantidadeItemLote-${idLote}-${numeroItemLote}`)
    inputQuantidadeItem.setAttribute(`data-quantidade`, 0)
    inputQuantidadeItem.setAttribute('onchange', `onChangeQuantidade(this, '${idLote}', '${numeroItemLote}')`)
    td4.appendChild(inputQuantidadeItem)

    let td5 = document.createElement('td')
    let inputValorItem = document.createElement('input')
    inputValorItem.setAttribute('class', 'form-control')
    inputValorItem.setAttribute('type', 'number')
    inputValorItem.setAttribute('step', "0.01")
    inputValorItem.setAttribute('id', `inputValorItemLote-${idLote}-${numeroItemLote}`)
    inputValorItem.setAttribute('onchange', `onChangeValor(this, '${idLote}', '${numeroItemLote}')`)

    td5.appendChild(inputValorItem)

    let td6 = document.createElement('td')

    let inputValorTotalItem = document.createElement('input')
    inputValorTotalItem.setAttribute('class', 'form-control')
    inputValorTotalItem.setAttribute('type', 'text')
    inputValorTotalItem.setAttribute('id', `inputValorTotalItemLote-${idLote}-${numeroItemLote}`)
    inputValorTotalItem.setAttribute(`data-valortotalitemlote-${idLote}`, `0`)
    inputValorTotalItem.disabled = true

    td6.appendChild(inputValorTotalItem)

    linhaLote.append(td0, td1, td2, td3, td4, td5, td6)

    return linhaLote

}

function onChangeQuantidade(inputQuantidade, idLote, numeroItemLote){
    processarInputQuantidade(inputQuantidade)
    calcularValorTotalItem(idLote, numeroItemLote)
    calcularValorTotalLote(idLote)
    removerClasseInvalido(inputQuantidade)

}


function onChangeValor(inputValor, idLote, numeroItemLote){

    calcularValorTotalItem(idLote, numeroItemLote)
    calcularValorTotalLote(idLote)
    removerClasseInvalido(inputValor)

}

function processarInputQuantidade_(inputCalcular) {
    // inverter a ordem, primeiro verificar match, depois se é numero.
    // Converte o valor para numérico no formato pt-BR
    let str_valor = inputCalcular.value.replace(',', '.')
    console.log('str_valor', str_valor)
    let  valorNumerico = parseFloat(str_valor);

    console.log("valorNumerico", valorNumerico, typeof valorNumerico)

    // Verifica se o valor é um número válido
    if (!isNaN(valorNumerico)) {
        console.log("Caso 1")
        inputCalcular.dataset.quantidade = valorNumerico

    } else {
        var expressao = inputCalcular.value

        // Expressão regular para encontrar o operador e os operandos
        var match = expressao.match(/([-]?\d{1,3}(?:\.\d{3})*)(?:,(\d+))?(?:([+\-*\/]))([-]?\d{1,3}(?:\.\d{3})*)(?:,(\d+))?/);

        if (match) {
            console.log("Caso 2")
            // Extrai os operandos e o operador
            var a = parseFloat(match[1].replace(/\./g, '').replace(',', '.'));
            var operador = match[3];
            var b = parseFloat(match[4].replace(/\./g, '').replace(',', '.'));

            // Calcula o resultado com base no operador
            var resultado;
            switch (operador) {
                case '+':
                    resultado = a + b;
                    break;
                case '-':
                    resultado = a - b;
                    break;
                case '*':
                    resultado = a * b;
                    break;
                case '/':
                    resultado = a / b;
                    break;
                default:
                    console.error('Operador inválido');
                    return;
            }

            console.log("valorNumerico", resultado, typeof resultado)

            inputCalcular['data-Quantidade'] = resultado

            // Define o valor do input como o resultado
            inputCalcular.value = resultado.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
        }else{
            console.log("Caso 4")
            // Se não for um número válido, define o valor do input como 0
            inputCalcular.dataset.quantidade = 0
            inputCalcular.value = 0;

        }

    }
}

function processarInputQuantidade(inputCalcular) {

    var expressao = inputCalcular.value

    // Expressão regular para encontrar o operador e os operandos
    var match = expressao.match(/([-]?\d{1,3}(?:\.\d{3})*)(?:,(\d+))?(?:([+\-*\/]))([-]?\d{1,3}(?:\.\d{3})*)(?:,(\d+))?/);

    if (match) {
        console.log("Caso 1")
        // Extrai os operandos e o operador
        var a = parseFloat(match[1].replace(/\./g, '').replace(',', '.'));
        var operador = match[3];
        var b = parseFloat(match[4].replace(/\./g, '').replace(',', '.'));

        // Calcula o resultado com base no operador
        var resultado;
        switch (operador) {
            case '+':
                resultado = a + b;
                break;
            case '-':
                resultado = a - b;
                break;
            case '*':
                resultado = a * b;
                break;
            case '/':
                resultado = a / b;
                break;
            default:
                console.error('Operador inválido');
                return;
        }

        inputCalcular.dataset.quantidade = resultado
        inputCalcular.value = resultado.toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
    }else{
        console.log("Caso 2")
        let str_valor = inputCalcular.value.replace(',', '.')
        let  valorNumerico = parseFloat(str_valor);

        if (!isNaN(valorNumerico)) {
            console.log("Caso 3")
            inputCalcular.value = valorNumerico.toLocaleString('pt-BR', { minimumFractionDigits: 2 });;
            inputCalcular.dataset.quantidade = valorNumerico
        } else {
            console.log("Caso 4")
            // Se não for um número válido, define o valor do input como 0
            inputCalcular.dataset.quantidade = 0
            inputCalcular.value = 0
        }
    }
}

function calcularValorTotalItem(idLote, numeroItemLote) {

    let inputQuantidade = document.getElementById(`inputQuantidadeItemLote-${idLote}-${numeroItemLote}`)
    console.log(inputQuantidade)

    let strQuantidade = inputQuantidade.dataset.quantidade
    let q =  Number(strQuantidade)
    console.log(q)
    let inputValor = document.getElementById(`inputValorItemLote-${idLote}-${numeroItemLote}`)
    let v = Number(inputValor.value)

    let vt = q*v

    let inputValorTotal = document.getElementById(`inputValorTotalItemLote-${idLote}-${numeroItemLote}`)
    inputValorTotal.value = vt.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
    inputValorTotal.setAttribute(`data-valortotalitemlote-${idLote}`, vt)
}


function calcularValorTotalLote(idLote) {
    let loteSelecionado = lotesLicitacao.find(obj=> obj.id==idLote)

    let colunaValorTotalLote = document.getElementById(`colunaValorTotalLote-${idLote}`)

    let valoresTotaisItens = document.querySelectorAll(`[data-valortotalitemlote-${idLote}]`)  //(`inputValorTotalItemLote-${idLote}`)
    console.log(`data-valortotalitemlote-${idLote}`, valoresTotaisItens)
    let valorTotal = 0

    for(let objetoValorTotalItem of valoresTotaisItens){
        let valorTotalItem = objetoValorTotalItem.getAttribute('data-valortotalitemlote-'+idLote)
        console.log(valorTotalItem)
        valorTotal += Number(valorTotalItem)
    }
    console.log("Calcular Valor Total do Lote", loteSelecionado)


    colunaValorTotalLote.innerHTML = valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
    // atualizar o atributo data-valortotallote para o valor total do lote
    colunaValorTotalLote.setAttribute(`data-valortotallote`, valorTotal)
    atualizarValorTotalLicitacao()

}

function somarValotTotalLote(idLote){
    let loteSelecionado = lotesLicitacao.find(obj=> obj.id==idLote)
    let valorTotalLote = 0
    let linhas = document.querySelectorAll(`[data-valorTotalItemLote-${idLote}]`)
    for(let i = 0; i < linhas.length; i++){
        valorTotalLote += Number(linhas[i].getAttribute('data-valorTotalItemLote-'+idLote))
    }

    return valorTotalLote
}


function atualizarValorTotalLicitacao(){
    let valorTotalLicitacao = document.getElementById('valor-total-licitacao')
    let valoresTotaisLotes = document.querySelectorAll('[data-valortotallote]')
    let valorTotal = 0

    for(let objetoValorTotalLote of valoresTotaisLotes){
        let valorTotalLote = objetoValorTotalLote.getAttribute('data-valortotallote')
        valorTotal += Number(valorTotalLote)
    }

    valorTotalLicitacao.innerHTML = valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
    valorTotalLicitacao.setAttribute('data-valortotallicitacao', valorTotal)
}

function criarTabelaItensLote(itens_lote, idLote, numeroLote) {

    let tabela = document.createElement('table')
    tabela.setAttribute('class', 'table table-sm table-striped')

    let cabecalhoTabela = document.createElement('thead')
    cabecalhoTabela.setAttribute('class', 'thead-light')

    let linhaCabecalhoSubtituloTabela = document.createElement('tr')
    //linhaCabecalhoSubtituloTabela.setAttribute('class', 'thead-light')
    let tituloCabecalho = document.createElement('strong')
    tituloCabecalho.appendChild(document.createTextNode('Dados da Licitação'))

    let tdLinhaCabecalhoTituloTabela = document.createElement('td')

    tdLinhaCabecalhoTituloTabela.setAttribute('colspan', '7')
    tdLinhaCabecalhoTituloTabela.style.textAlign = "center"
    tdLinhaCabecalhoTituloTabela.style.backgroundColor = "rgba(0, 0, 0, 0.15)"
    tdLinhaCabecalhoTituloTabela.appendChild(tituloCabecalho)
    //tdLinhaCabecalhoTituloTabela.setAttribute('class', 'table-light')
    linhaCabecalhoSubtituloTabela.appendChild(tdLinhaCabecalhoTituloTabela)

    let linhaCabecalhoTabela = document.createElement('tr')
    let c1CabecalhoTabela = document.createElement('th')
    c1CabecalhoTabela.style.width = "4%"

    let iconeAdicionarItem = document.createElement('i')
    iconeAdicionarItem.setAttribute('class', 'fa-solid fa-plus')

    iconeAdicionarItem.setAttribute("data-toggle", "tooltip")
    iconeAdicionarItem.setAttribute("data-placement", "top")
    iconeAdicionarItem.setAttribute("title", `Adicionar item ao lote`)
    iconeAdicionarItem.setAttribute('onclick', `adicionarItemLote('${idLote}')`)

    iconeAdicionarItem.style.cursor = 'pointer'

    console.log(edicaoFinalizada)
    if(edicaoFinalizada === false){
        c1CabecalhoTabela.appendChild(iconeAdicionarItem)
        c1CabecalhoTabela.appendChild(document.createTextNode(" "))
    }

    let c2CabecalhoTabela = document.createElement('th')
    c2CabecalhoTabela.style.width = "5rem"
    c2CabecalhoTabela.appendChild(document.createTextNode("Item"))
    let c3CabecalhoTabela = document.createElement('th')
    c3CabecalhoTabela.appendChild(document.createTextNode("Descrição"))

    let c4CabecalhoTabela = document.createElement('th')
    c4CabecalhoTabela.appendChild(document.createTextNode("Un. Medida"))
    c4CabecalhoTabela.style.width = "10rem"

    let c5CabecalhoTabela = document.createElement('th')
    c5CabecalhoTabela.style.width = "8rem"
    c5CabecalhoTabela.appendChild(document.createTextNode("Quantidade"))
    let c6CabecalhoTabela = document.createElement('th')
    c6CabecalhoTabela.style.width = "8rem"
    c6CabecalhoTabela.appendChild(document.createTextNode("Valor"))
    let c7CabecalhoTabela = document.createElement('th')
    c7CabecalhoTabela.style.width = "10rem"
    c7CabecalhoTabela.appendChild(document.createTextNode("Valor Total"))

    linhaCabecalhoTabela.appendChild(c1CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c2CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c3CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c4CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c5CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c6CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c7CabecalhoTabela)

    cabecalhoTabela.appendChild(linhaCabecalhoSubtituloTabela)
    cabecalhoTabela.appendChild(linhaCabecalhoTabela)

    let corpoTabela = document.createElement('tbody')
    corpoTabela.setAttribute('id', `ItensTabelaLote-${idLote}`)

    for(let itemLoteLicitacao of itens_lote){

        let linha_itemLote = criarLinhaItemLote(itemLoteLicitacao, idLote)
        corpoTabela.appendChild(linha_itemLote)

    }

    tabela.appendChild(cabecalhoTabela)

    tabela.appendChild(corpoTabela)

    return tabela
}


function criarLinhaLote(lote) {

    let linhaLote = document.createElement('div')
    linhaLote.setAttribute('class', 'row')
    linhaLote.style.paddingTop = "1rem"
    linhaLote.style.paddingBottom = "1rem"
    linhaLote.setAttribute('id', `linhaLoteLicitacao-${lote['id']}`)
    linhaLote.setAttribute('data-numeroLote', `${lote['numero_lote']}`)

    let colunaConteudoLote = document.createElement('div')
    colunaConteudoLote.setAttribute('class', 'col')

    let linhaDadosLote = document.createElement('div')
    linhaDadosLote.setAttribute('class', 'row')

    let linhaItensLote = document.createElement('div')
    linhaItensLote.setAttribute('class', 'row')

    let coluna1DadosLote = document.createElement('div')
    coluna1DadosLote.setAttribute('class', 'col-2')
    let conteudoColuna1DadosLote = document.createElement('strong')
    conteudoColuna1DadosLote.appendChild(document.createTextNode('Lote: '))
    coluna1DadosLote.appendChild(conteudoColuna1DadosLote)
    coluna1DadosLote.appendChild(document.createTextNode(lote['numero_lote']))

    let coluna2DadosLote = document.createElement('div')
    coluna2DadosLote.setAttribute('class', 'col-3')

    let conteudoColuna2DadosLote = document.createElement('strong')
    conteudoColuna2DadosLote.appendChild(document.createTextNode('Descrição do Lote: '))
    coluna2DadosLote.appendChild(conteudoColuna2DadosLote)
    coluna2DadosLote.appendChild(document.createTextNode(lote['descricao_lote']))

    let coluna3DadosLote = document.createElement('div')
    coluna3DadosLote.setAttribute('class', 'col-2')
    let conteudoColuna3DadosLote = document.createElement('strong')
    conteudoColuna3DadosLote.appendChild(document.createTextNode('Valor Total do Lote: '))
    // alinhar texto á direita
    coluna3DadosLote.style.textAlign = "right"

    coluna3DadosLote.appendChild(conteudoColuna3DadosLote)

    let coluna4DadosLote = document.createElement('div')
    coluna4DadosLote.setAttribute('class', 'col-2')
    coluna4DadosLote.setAttribute('id', `colunaValorTotalLote-${lote['id']}`)
    coluna4DadosLote.setAttribute('data-tipoColuna', 'valorTotalLote')
    coluna4DadosLote.setAttribute('data-valorTotalLote', '0')


    let coluna5DadosLote = document.createElement('div')
    coluna5DadosLote.setAttribute('class', 'col-1')

    let coluna6DadosLote = document.createElement('div')
    coluna6DadosLote.setAttribute('class', 'col-2')

    let funcaoExcluirIcone = `excluirLoteLicitacao('${lote['id']}')`

    let iconeEscluirLote = document.createElement('i')
    iconeEscluirLote.setAttribute('class', 'far fa-trash-alt')
    iconeEscluirLote.style.cursor = 'pointer'
    iconeEscluirLote.style.position = 'absolute'
    iconeEscluirLote.style.right = '30px'
    iconeEscluirLote.style.color = 'red'
    iconeEscluirLote.setAttribute('onclick', funcaoExcluirIcone)

    //se a variavel edicaoFinalizada for falsa, então o usuário pode excluir o lote
    if(!edicaoFinalizada){
        coluna5DadosLote.appendChild(iconeEscluirLote)
    }


    linhaDadosLote.appendChild(coluna1DadosLote)
    linhaDadosLote.appendChild(coluna2DadosLote)
    linhaDadosLote.appendChild(coluna6DadosLote)
    linhaDadosLote.appendChild(coluna3DadosLote)
    linhaDadosLote.appendChild(coluna4DadosLote)
    linhaDadosLote.appendChild(coluna5DadosLote)

    let tabelaItensLote = criarTabelaItensLote(lote['itens_lote'], lote['id'], lote['numero_lote'])

    linhaItensLote.appendChild(tabelaItensLote)

    colunaConteudoLote.appendChild(linhaDadosLote)
    colunaConteudoLote.appendChild(linhaItensLote)


    linhaLote.appendChild(colunaConteudoLote)

    return linhaLote

}


function atualizarValorTotalLote(idLote){
    let colunaValorTotalLote = document.getElementById(`colunaValorTotalLote-${idLote}`)
    let valorTotalLoteAtualizado = somarValotTotalLote(idLote)
    // se colunaValorTotalLote possuir texto , então remove-o, depois atualiza o valor total do lote
    if(colunaValorTotalLote.textContent !== ""){
        colunaValorTotalLote.removeChild(colunaValorTotalLote.firstChild)
    }
    colunaValorTotalLote.innerHTML =  `${valorTotalLoteAtualizado.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'})}`
    colunaValorTotalLote.setAttribute(`data-valortotallote`, valorTotalLoteAtualizado)

}

function proximoNumeroLote(){
    numeroUltimoLote += 1
    return numeroUltimoLote
}

function novoLote(){

    const idModal = 'modalNovoLote'

    if(document.getElementById(idModal)){
        let modal = new bootstrap.Modal(document.getElementById(idModal))
        modal.show()
    }else{

        let conteudoModal = criarConteudoModalNovoLote()
        let janela_modal = criarModal(idModal, 'Novo Lote', conteudoModal, "modal-lg")
        document.body.appendChild(janela_modal)
        let modal = new bootstrap.Modal(janela_modal)
        modal.show()
    }

}

function criarConteudoModalNovoLote(){
    let modalBody = document.createElement('div')
    modalBody.setAttribute('class', 'modal-body')

    let formNovoLote = criarFormularioBase("cadastrarNovoLote")

    let linhaCabecalho = document.createElement('div')
    linhaCabecalho.setAttribute('class', 'row')
    linhaCabecalho.style.marginBottom = "25px"


    let colunaCabecalhoNumero = document.createElement('div')
    colunaCabecalhoNumero.setAttribute('class', 'col-2')
    colunaCabecalhoNumero.textContent = "Numero"

    let colunaCabecalhoDescricao = document.createElement('div')
    colunaCabecalhoDescricao.setAttribute('class', 'col-9')
    colunaCabecalhoDescricao.textContent = "Descrição"

    let colunaCabecalhoAdicionar = document.createElement('div')
    colunaCabecalhoAdicionar.setAttribute('class', 'col-1')

    let iconeAdicionar = document.createElement("i")
    iconeAdicionar.className = "fa-solid fa-plus"
    iconeAdicionar.style.color = "green"
    iconeAdicionar.style.cursor = 'pointer'
    iconeAdicionar.setAttribute("onclick", "adicionarNovaLinhaLoteFormulario()")

    colunaCabecalhoAdicionar.append(iconeAdicionar)


    linhaCabecalho.append(colunaCabecalhoAdicionar, colunaCabecalhoNumero, colunaCabecalhoDescricao)

    let formGroupLotes = document.createElement('div')
    formGroupLotes.id = "idformGroupLotes"

    let linhaLote = criarLinhaFormularioLote()

    formGroupLotes.appendChild(linhaLote)

    let formGroupSalvarLote = document.createElement('div')

    let buttonSalvarLote = document.createElement('button')
    buttonSalvarLote.setAttribute('type', 'submit')
    buttonSalvarLote.setAttribute('class', 'btn btn-primary')
    buttonSalvarLote.style.marginTop = "10px"
    buttonSalvarLote.appendChild(document.createTextNode('Salvar'))

    formGroupSalvarLote.appendChild(buttonSalvarLote)
    formNovoLote.appendChild(linhaCabecalho)
    formNovoLote.appendChild(formGroupLotes)
    formNovoLote.appendChild(formGroupSalvarLote)

    modalBody.appendChild(formNovoLote)

    return modalBody
}

function criarLinhaFormularioLote(){
    let linhaLote = document.createElement('div')
    linhaLote.setAttribute('class', 'row')
    linhaLote.style.marginBottom = "8px"

    let colunaNumeroLote = document.createElement('div')
    colunaNumeroLote.className = "col-2"

    let colunaDescricao = document.createElement('div')
    colunaDescricao.className = "col-9"

    let colunaExcluir = document.createElement('div')
    colunaExcluir.className = "col-1"


    let inputNumeroLote = document.createElement('input')
    inputNumeroLote.setAttribute('type', 'number')
    inputNumeroLote.setAttribute('class', 'form-control')
    inputNumeroLote.setAttribute('id', 'numeroLote')
    inputNumeroLote.setAttribute('name', 'numeroLote')
    inputNumeroLote.value = proximoNumeroLote()
    inputNumeroLote.required = true

    colunaNumeroLote.appendChild(inputNumeroLote)

    let inputDescricaoLote = document.createElement('input')
    inputDescricaoLote.setAttribute('type', 'text')
    inputDescricaoLote.setAttribute('class', 'form-control')
    inputDescricaoLote.setAttribute('id', 'descricaoLote')
    inputDescricaoLote.setAttribute('name', 'descricaoLote')
    inputDescricaoLote.setAttribute('placeholder', 'Descrição do Lote')
    inputDescricaoLote.required = true

    colunaDescricao.appendChild(inputDescricaoLote)

    let iconeExcluir = document.createElement('i')
    iconeExcluir.className = "fa-solid fa-minus"
    iconeExcluir.style.color = "red"

    colunaExcluir.appendChild(iconeExcluir)

    linhaLote.append(colunaExcluir, colunaNumeroLote, colunaDescricao)

    return linhaLote
}

function adicionarNovaLinhaLoteFormulario(){
    let linha = criarLinhaFormularioLote()
    let inputGroupLotes = document.getElementById('idformGroupLotes')
    inputGroupLotes.append(linha)

}