function criarTabelasLotes(tipo, id){
    colunaLotes = document.getElementById('coluna-lotes-contratados')
    // remove all child nodes of colunaLotes
    while (colunaLotes.firstChild) {
        colunaLotes.removeChild(colunaLotes.firstChild);
    }

    // filtrar a variavel visualizacoes pelos valores das chaves tipo e id
    visualizacao = visualizacoes.filter(v => v.tipo == tipo && v.id == id)[0]

    if(visualizacao.tipo === "contrato"){
        let containerLotes = criarContainerlLotesContratados(lotes_contratados, visualizacao.editavel, visualizacao.aditivo_quantidade)
        let valorTotal = calcularValorTotalLotes(containerLotes)
        colunaLotes.appendChild(containerLotes)
        if(!visualizacao.editavel){
            if(!visualizacao.aditivo_quantidade){
                //colunaLotes.append(criarContainerControleItensFaturas(visualizacao.controle_faturas_contrato, visualizacao.controleFaturasProducao))
            }else if(!visualizacao.aditivo_quantidade.editavel){
                //colunaLotes.append(criarContainerControleItensFaturas(visualizacao.controle_faturas_contrato, visualizacao.controleFaturasProducao))
            }
        }
    }else if(visualizacao.tipo === "aditivo"){
        //let ContainerLotesAditivados = criarContainerLotesAditivados(lotes_contratados)
        let containerLotes = criarContainerlLotesAditivados(
            visualizacao.lotes_visualizacao, visualizacao.editavel, visualizacao.id, visualizacao.aditivo_quantidade)
        let valorTotal = calcularValorTotalLotes(containerLotes)
        colunaLotes.append(containerLotes)
        if(!visualizacao.editavel){
            if(!visualizacao.aditivo_quantidade){
                //colunaLotes.append(criarContainerControleItensFaturas(visualizacao.controle_faturas_contrato, visualizacao.controleFaturasProducao))
            }else if(!visualizacao.aditivo_quantidade.editavel){
                //colunaLotes.append(criarContainerControleItensFaturas(visualizacao.controle_faturas_contrato, visualizacao.controleFaturasProducao))
            }
        }
    }else if(visualizacao.tipo === "profissional"){
        profissionaisContratados = visualizacao['profissionais_habilitaveis']
        colunaLotes.append(
            criarContainerProfissionais(visualizacao.profissionais_habilitados, visualizacao.editavel,
                visualizacao.itens_habilitaveis_profissional))
    }
}


function visualizarLotes(tipo, id){
    alternarVisualizacaoAtiva(tipo, id)
    criarTabelasLotes(tipo, id)
}

function alternarVisualizacaoAtiva(tipo, id){
    let navLinks = document.getElementsByClassName('pill-view')
    for(var navLink of navLinks){
        navlinkID = navLink.getAttribute('id');
        if(navlinkID === `link-${tipo}-${id}`){
            document.getElementById(navlinkID).className = 'pill-view nav-link active disabled'
        }else{
            document.getElementById(navlinkID).className = 'pill-view nav-link'
        }
    }

}


function criarContainerlLotesContratados(lotesContratados, editavel, aditivoQuantidade) {
    let container = document.createElement('div');
    container.classList.add('container-fluid');
    container.setAttribute('id', 'container-lotes-contratados');


    for(let loteContratado of lotesContratados){
        container.append(criarLinhaLoteContratado(loteContratado, editavel, aditivoQuantidade));
    }

    return container;

}

function criarLinhaLoteContratado(loteContratado, editavel, aditivoQuantidade) {
    let linhaLote = document.createElement('div')
    linhaLote.setAttribute('class', 'row')
    linhaLote.style.paddingTop = "1rem"
    linhaLote.style.paddingBottom = "1rem"
    linhaLote.setAttribute('id', `linhaLoteContratado-${loteContratado['id']}`)
    linhaLote.setAttribute('data-numeroLote', `${loteContratado['numero_lote']}`)

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
        iconeExcluir.setAttribute('onclick', `excluirLoteContratado(${loteContratado['id']})`)
        coluna3DadosLote.appendChild(iconeExcluir)
        // alinhar iconeExcluir á direita
        coluna3DadosLote.style.textAlign = "right"
    }

    let conteudoColuna1DadosLote = document.createElement('strong')
    conteudoColuna1DadosLote.appendChild(document.createTextNode(`Lote ${loteContratado['numero_lote']} - ${loteContratado['descricao_lote']}`))

    let tabelaItensLoteContrato = criarTabelaItensLoteContrato(
        loteContratado['itens_vinculados'], loteContratado['itens_vinculaveis'], loteContratado['id'],
        loteContratado['numero_lote'], editavel, aditivoQuantidade)
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


function criarTabelaItensLoteContrato(
    itensLoteContratoVinculados, itensLoteContratoVinculaveis, idLote, numeroLote,editavel, aditivoQuantidade){
    if(editavel){tcs = 7}else{tcs = 9}
    let tabela = document.createElement('table')
    tabela.setAttribute('class', 'table table-sm table-striped')
    let cabecalhoTabela = document.createElement('thead')
    cabecalhoTabela.setAttribute('class', 'thead-light')

    let linhaTituloTabela = document.createElement('tr')
    let tituloCabecalho = document.createElement("strong")
    tituloCabecalho.appendChild(document.createTextNode("Itens Contratados"))
    let tdLinhaCabecalhoTituloTabela = document.createElement('td')
    tdLinhaCabecalhoTituloTabela.setAttribute('colspan', `${tcs}`)
    tdLinhaCabecalhoTituloTabela.style.textAlign = "center"
    tdLinhaCabecalhoTituloTabela.style.backgroundColor = "rgba(171, 206, 211, 1)"
    tdLinhaCabecalhoTituloTabela.appendChild(tituloCabecalho)
    tdLinhaCabecalhoTituloTabela.style.width = "1rem"

    linhaTituloTabela.appendChild(tdLinhaCabecalhoTituloTabela)

    let linhaCabecalhoTabela = document.createElement('tr')

    let c2CabecalhoTabela = document.createElement('th')
    c2CabecalhoTabela.style.width = "5%"
    c2CabecalhoTabela.appendChild(document.createTextNode("Item"))
    let c3CabecalhoTabela = document.createElement('th')
    c3CabecalhoTabela.appendChild(document.createTextNode("Descrição"))
    let c4CabecalhoTabela = document.createElement('th')
    c4CabecalhoTabela.style.width = "15%"
    c4CabecalhoTabela.appendChild(document.createTextNode("Unidade Medida"))
    let c5CabecalhoTabela = document.createElement('th')
    c5CabecalhoTabela.style.width = "8%"
    c5CabecalhoTabela.appendChild(document.createTextNode("Quant. Cont."))
    let c6CabecalhoTabela = document.createElement('th')
    c6CabecalhoTabela.style.width = "8%"
    c6CabecalhoTabela.appendChild(document.createTextNode("Valor Un."))
    let c7CabecalhoTabela = document.createElement('th')
    c7CabecalhoTabela.style.width = "10%"
    c7CabecalhoTabela.appendChild(document.createTextNode("Valor Total"))

    let c8CabecalhoTabela = document.createElement('th')
    c8CabecalhoTabela.style.width = "3%"


    linhaCabecalhoTabela.appendChild(c2CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c3CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c4CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c5CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c6CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c7CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c8CabecalhoTabela)

    if(!editavel){
        let c9CabecalhoTabela = document.createElement('th')
        c9CabecalhoTabela.style.width = "12%"
        c9CabecalhoTabela.appendChild(document.createTextNode("Valor Faturado"))
        let c10CabecalhoTabela = document.createElement('th')
        c10CabecalhoTabela.style.width = "10%"
        c10CabecalhoTabela.appendChild(document.createTextNode("Saldo"))

        linhaCabecalhoTabela.appendChild(c9CabecalhoTabela)
        linhaCabecalhoTabela.appendChild(c10CabecalhoTabela)

    }
    cabecalhoTabela.appendChild(linhaTituloTabela)
    cabecalhoTabela.appendChild(linhaCabecalhoTabela)

    let corpoTabela = document.createElement('tbody')
    corpoTabela.setAttribute('id', `ItensTabelaLote-${idLote}`)

    for(itemContratoVinculado of itensLoteContratoVinculados){
        console.log('itemContratoVinculado', itemContratoVinculado)
        let linhaItemTabela = criarLinhaTabelaItens(true, itemContratoVinculado, editavel, aditivoQuantidade, idLote)


        corpoTabela.appendChild(linhaItemTabela)

    }

    let itensValorTotal = corpoTabela.querySelectorAll('td[id="tdValorTotalItem"]')
    let itensValorFaturado = corpoTabela.querySelectorAll('td[id="tdValorFaturadoItem"]')
    valorTotalContratadoLote = 0
    for(ivt of itensValorTotal){valorTotalContratadoLote += Number(ivt.getAttribute('data-ValorTotalItem'))}

    valorTotalFaturadoLote = 0
    for(ivf of itensValorFaturado){valorTotalFaturadoLote += Number(ivf.getAttribute('data-ValorFaturadoItem'))}

    if(statusContrato === "cadastro"){
        for(itemContratoVinculavel of itensLoteContratoVinculaveis){
            let linhaItemTabela = criarLinhaTabelaItens(false, itemContratoVinculavel, editavel, aditivoQuantidade, idLote)
            corpoTabela.appendChild(linhaItemTabela)

        }
    }
    tabela.appendChild(cabecalhoTabela)
    tabela.appendChild(corpoTabela)
    tabela.appendChild(criarRodapeTotalLote(valorTotalContratadoLote, valorTotalFaturadoLote, editavel, idLote))

    return tabela
}

function criarRodapeTotalLote(totalContratadoLote, totalFaturadoLote, editavel, idLote){
    let saldo = totalContratadoLote - totalFaturadoLote
    let tf = document.createElement('tfoot')

    let tr = document.createElement('tr')
    tr.setAttribute('class', 'table-info')

    let th1 = document.createElement('th')
    th1.appendChild(document.createTextNode("Valor Total: "))
    th1.colSpan = 2
    let td1 = document.createElement('td')
    td1.setAttribute('id', 'tdValorTotalContratadoLote') //tdValorTotalContratadoLote
    td1.setAttribute('data-idLoteValorTotalContratadoLote', idLote)
    td1.setAttribute('data-ValorTotalContratadoLote', totalContratadoLote)
    td1.appendChild(document.createTextNode(
        `${totalContratadoLote.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`
    ))

    let th2 = document.createElement('th')

    th2.appendChild(document.createTextNode("Total Faturado: "))
    th2.colSpan = 2

    let td2 = document.createElement('td')
    td2.setAttribute('id', 'tdValorTotalFaturadoLote')
    td2.setAttribute('data-ValorTotalFaturadoLote', totalFaturadoLote)
    td2.appendChild(document.createTextNode(
        `${totalFaturadoLote.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`
    ))

    let th3 = document.createElement('th')
    th3.appendChild(document.createTextNode("Saldo: "))
    th3.colSpan = 2
    let td3 = document.createElement('td')
    td3.appendChild(document.createTextNode(
        `${saldo.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`
    ))

    tr.appendChild(th1)
    tr.appendChild(td1)
    if(!editavel){
        tr.appendChild(th2)
        tr.appendChild(td2)
        tr.appendChild(th3)
        tr.appendChild(td3)
    }
    tf.appendChild(tr)
    return tf

}

///////////////////// Aba Profissionais habilitados /////////////////////////
function criarTabelaItensLoteAditivado(itensLoteContratoVinculados, itensLoteContratoVinculaveis,
                                       idLote, numeroLote, editavel, idAditivo, aditivoQuantidade){
    console.log("criarTabelaItensLoteAditivado - AQ", aditivoQuantidade)

    if(editavel){tcs = 7}else{tcs = 9}
    let tabela = document.createElement('table')
    tabela.setAttribute('class', 'table table-sm table-striped')
    let cabecalhoTabela = document.createElement('thead')
    cabecalhoTabela.setAttribute('class', 'thead-light')

    let linhaTituloTabela = document.createElement('tr')
    let tituloCabecalho = document.createElement("strong")
    tituloCabecalho.appendChild(document.createTextNode("Itens Aditivados"))
    let tdLinhaCabecalhoTituloTabela = document.createElement('td')
    tdLinhaCabecalhoTituloTabela.setAttribute('colspan', `${tcs}`)
    tdLinhaCabecalhoTituloTabela.style.textAlign = "center"
    tdLinhaCabecalhoTituloTabela.style.backgroundColor = "rgba(171, 206, 211, 1)"
    tdLinhaCabecalhoTituloTabela.appendChild(tituloCabecalho)
    tdLinhaCabecalhoTituloTabela.style.width = "1rem"

    linhaTituloTabela.appendChild(tdLinhaCabecalhoTituloTabela)

    let linhaCabecalhoTabela = document.createElement('tr')

    let c2CabecalhoTabela = document.createElement('th')
    c2CabecalhoTabela.style.width = "5%"
    c2CabecalhoTabela.appendChild(document.createTextNode("Item"))
    let c3CabecalhoTabela = document.createElement('th')
    c3CabecalhoTabela.appendChild(document.createTextNode("Descrição"))

    let c4CabecalhoTabela = document.createElement('th')
    c4CabecalhoTabela.appendChild(document.createTextNode("Unidade Medida"))
    c4CabecalhoTabela.style.width = "15%"

    let c5CabecalhoTabela = document.createElement('th')
    c5CabecalhoTabela.style.width = "8%"
    c5CabecalhoTabela.appendChild(document.createTextNode("Quant. Cont."))
    let c6CabecalhoTabela = document.createElement('th')
    c6CabecalhoTabela.style.width = "8%"
    c6CabecalhoTabela.appendChild(document.createTextNode("Valor Un."))
    let c7CabecalhoTabela = document.createElement('th')
    c7CabecalhoTabela.style.width = "10%"
    c7CabecalhoTabela.appendChild(document.createTextNode("Valor Total"))

    let c8CabecalhoTabela = document.createElement('th')
    c8CabecalhoTabela.style.width = "3%"

    let c9CabecalhoTabela = document.createElement('th')
    c9CabecalhoTabela.style.width = "12%"
    c9CabecalhoTabela.appendChild(document.createTextNode("Valor Faturado"))

    let c10CabecalhoTabela = document.createElement('th')
    c10CabecalhoTabela.style.width = "10%"
    c10CabecalhoTabela.appendChild(document.createTextNode("Saldo"))

    linhaCabecalhoTabela.appendChild(c2CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c3CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c4CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c5CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c6CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c7CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c8CabecalhoTabela)
    if(!editavel){
        linhaCabecalhoTabela.appendChild(c9CabecalhoTabela)
        linhaCabecalhoTabela.appendChild(c10CabecalhoTabela)
    }

    cabecalhoTabela.append(linhaTituloTabela, linhaCabecalhoTabela)

    let corpoTabela = document.createElement('tbody')
    corpoTabela.setAttribute('id', `ItensTabelaLote-${idLote}`)

    for(itemContratoVinculado of itensLoteContratoVinculados){
        //vinculado, item, editavel, idAditivo, aditivoQuantidade
        let linhaItemTabela = criarLinhaTabelaItensAditivados(true, itemContratoVinculado, editavel, idAditivo,
            aditivoQuantidade, idLote)


        corpoTabela.appendChild(linhaItemTabela)

    }
    if(editavel){
        for(itemContratoVinculavel of itensLoteContratoVinculaveis){
            let linhaItemTabela = criarLinhaTabelaItensAditivados(false, itemContratoVinculavel, editavel,
                idAditivo, aditivoQuantidade, idLote)
            corpoTabela.appendChild(linhaItemTabela)

        }
    }

    tabela.appendChild(cabecalhoTabela)

    let itensValorTotal = corpoTabela.querySelectorAll('td[id="tdValorTotalItem"]')
    let itensValorFaturado = corpoTabela.querySelectorAll('td[id="tdValorFaturadoItem"]')

    valorTotalContratadoLote = 0
    for(ivt of itensValorTotal){valorTotalContratadoLote += Number(ivt.getAttribute('data-ValorTotalItem'))}
    valorTotalFaturadoLote = 0
    for(ivf of itensValorFaturado){valorTotalFaturadoLote += Number(ivf.getAttribute('data-ValorFaturadoItem'))}
    tabela.appendChild(corpoTabela)
    tabela.appendChild(criarRodapeTotalLote(valorTotalContratadoLote, valorTotalFaturadoLote, editavel, idLote))


    return tabela

}

function criarTabelaProfissionaisHabilitados(profissionaisHabilitados, editavel, itensHabilitaveis){
    let tabela = document.createElement('table')
    tabela.setAttribute('class', 'table table-sm table-striped')
    let cabecalhoTabela = document.createElement('thead')
    cabecalhoTabela.setAttribute('class', 'thead-light')

    let linhaCabecalhoTabela = document.createElement('tr')

    let c2CabecalhoTabela = document.createElement('th')
    c2CabecalhoTabela.style.width = "5%"
    c2CabecalhoTabela.appendChild(document.createTextNode(""))

    let c3CabecalhoTabela = document.createElement('th')
    c3CabecalhoTabela.appendChild(document.createTextNode("Nome"))

    let c4CabecalhoTabela = document.createElement('th')
    c4CabecalhoTabela.appendChild(document.createTextNode("Conselho"))
    c4CabecalhoTabela.style.width = "15%"

    linhaCabecalhoTabela.appendChild(c2CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c3CabecalhoTabela)
    linhaCabecalhoTabela.appendChild(c4CabecalhoTabela)
    console.log("IHS: ", itensHabilitaveis)
    for(ih of itensHabilitaveis){
        console.log("IH: ")
        let colCabecalhoItem = document.createElement('th')
        colCabecalhoItem.style.maxWidth = "4rem"
        colCabecalhoItem.appendChild(document.createTextNode(`L${ih['numeroLote']}-I${ih['numeroItem']}`))
        linhaCabecalhoTabela.appendChild(colCabecalhoItem)

    }

    cabecalhoTabela.appendChild(linhaCabecalhoTabela)

    let corpoTabela = document.createElement('tbody')
    corpoTabela.setAttribute('id', `profissionaisHabilitados`)

    for(profissionalHabilitado of profissionaisHabilitados){
        let lp = criarLinhaProfissionalVinculado(profissionalHabilitado, editavel, itensHabilitaveis)
        corpoTabela.appendChild(lp)
    }

    tabela.appendChild(cabecalhoTabela)

    tabela.appendChild(corpoTabela)

    return tabela

}

function criarLinhaProfissionalVinculado(profissionalHabilitado, editavel, itensHabilitaveis){

    let linhaItemTabela = document.createElement('tr')
    let td2 = document.createElement('td')

    let td3 = document.createElement('td')
    td3.appendChild(document.createTextNode(`${profissionalHabilitado.nome}`))
    let td4 = document.createElement('td')
    td4.appendChild(document.createTextNode(`${profissionalHabilitado.conselho}/${profissionalHabilitado.estado_conselho} - ${profissionalHabilitado.numero_conselho}`))

    if(editavel){
        let iconeExcluir = document.createElement('i')
        iconeExcluir.setAttribute('class', 'fas fa-trash-alt')
        iconeExcluir.style.cursor = "pointer"
        iconeExcluir.style.color = "red"
        iconeExcluir.setAttribute('onclick', `excluirProfissionalHabilitado(${profissionalHabilitado.id})`)
        td2.appendChild(iconeExcluir)
    }

    linhaItemTabela.appendChild(td2)
    linhaItemTabela.appendChild(td3)
    linhaItemTabela.appendChild(td4)

    let habilitacoesProfissional = profissionalHabilitado.itens_habilitados
    console.log("GP: ", habilitacoesProfissional)
    for(ih of itensHabilitaveis){
        let tdIh = document.createElement('td')

        let divcheckItemProfissional = document.createElement('div')
        divcheckItemProfissional.setAttribute('class', 'form-check')
        let checkItemProfissional = document.createElement('input')
        checkItemProfissional.setAttribute('class', 'form-check-input')
        checkItemProfissional.type = 'checkbox'

        checkItemProfissional.setAttribute('data-idLoteContratoCheckProfissional', ih['idLoteContrato'])
        checkItemProfissional.setAttribute('data-numeroLoteCheckProfissional', ih['numeroLote'])
        checkItemProfissional.setAttribute('data-idItemContratoCheckProfissional', ih['idItemContrato'])
        checkItemProfissional.setAttribute('data-idItemLicitacaoCheckProfissional', ih['idItemLicitacao'])
        checkItemProfissional.setAttribute('data-numeroItemCheckProfissional', ih['numeroItem'])
        checkItemProfissional.setAttribute('data-checkItemProfissionalidProfissional', profissionalHabilitado.id)
        checkItemProfissional.setAttribute('onclick', `atualizarHabilitacaoProfissional(this)`)

        let habilitacaoItem = habilitacoesProfissional.filter(f => f.idItemLicitacao == ih['idItemLicitacao'])

        if(habilitacaoItem.length > 0){
            checkItemProfissional.checked = true
        }


        divcheckItemProfissional.appendChild(checkItemProfissional)
        tdIh.appendChild(divcheckItemProfissional)
        linhaItemTabela.appendChild(tdIh)
    }

    let tdSync = document.createElement('td')


    tdSync.setAttribute('class', 'fas fa-sync-alt')
    tdSync.setAttribute('id', `iconeAtualizarHabilitacaoProfissional-${profissionalHabilitado.id}`)
    tdSync.setAttribute('onclick', `EnviarHabilitacaoProfissional('${profissionalHabilitado.id}')`)
    tdSync.style.color = 'green'
    tdSync.style.cursor = 'pointer'

    linhaItemTabela.appendChild(tdSync)

    return linhaItemTabela
}


function calcularValorTotalLoteContratado(idLote){

    let valorTotalLote = 0
    let tdValoresTotaisItens = document.querySelectorAll(`td[data-idLoteValorTotalItem="${idLote}"]`)
    for(v of tdValoresTotaisItens){
        valorTotalLote += Number(v.getAttribute('data-valorTotalItem'))
    }
    return valorTotalLote

}

function calcularValorTotalLotes(Containerlotes){
    let lotesValorTotalContratado = Containerlotes.querySelectorAll('td[id="tdValorTotalContratadoLote"]')
    let lotesValorTotalFaturado = Containerlotes.querySelectorAll('td[id="tdValorTotalFaturadoLote"]')

    valorTotalContratado = 0
    valorTotalFaturado = 0

    for(l of lotesValorTotalContratado){valorTotalContratado += Number(l.getAttribute('data-ValorTotalContratadoLote'))}
    for(l of lotesValorTotalFaturado){valorTotalFaturado += Number(l.getAttribute('data-ValorTotalFaturadoLote'))}

    return [valorTotalContratado, valorTotalFaturado]
}

function criarContainerControleItensFaturas(controleFaturasContrato, controleFaturasProducao){
    let containerFaturas = document.createElement('div')
    containerFaturas.setAttribute('class', 'container-fluid')
    containerFaturas.setAttribute('id', 'container-faturas')

    let linhaTabelaFaturas = criarLinhaTituloTabelaFaturas('Escala')

    containerFaturas.appendChild(linhaTabelaFaturas)

    let linhaConteudoTabelaFaturas = document.createElement('div')
    linhaConteudoTabelaFaturas.setAttribute('class', 'row')
    linhaConteudoTabelaFaturas.setAttribute('id', 'linha-cabecalho-tabela-faturas')

    let tabelaFaturas = document.createElement('table')
    tabelaFaturas.setAttribute('class', 'table table-sm table-striped')

    let tabelaResumoFaturas = document.createElement('table')
    tabelaResumoFaturas.setAttribute('class', 'table table-sm table-striped')

    let cabecalhoTabelaFaturas = document.createElement('thead')
    cabecalhoTabelaFaturas.setAttribute('class', 'thead-light')

    let linhaCabecalhoTabelaFaturas = document.createElement('tr')
    let linha2CabecalhoTabelaFaturas = document.createElement('tr')

    let c1Th = document.createElement('th')
    c1Th.innerHTML = `Fatura`
    c1Th.style.minWidth = "140px"
    c1Th.style.verticalAlign = "middle"
    c1Th.rowSpan= 2
    linhaCabecalhoTabelaFaturas.appendChild(c1Th)

    for(ill of controleFaturasContrato[1]){
        let cth =  document.createElement('th')
        cth.innerHTML = `${ill.numero_lote}.${ill.numero_item} - ${ill.especialidade}
            <br>${
            ill.descricao_item
        }`
        cth.style.minWidth = "140px"
        cth.style.textAlign = "center"
        cth.colSpan = 2
        // definir borda da coluna
        cth.style.borderLeft = "1px solid #ccc"
        linhaCabecalhoTabelaFaturas.appendChild(cth)

        let cth1L2 =  document.createElement('th')
        cth1L2.innerHTML = `Horas Item`
        cth1L2.style.borderLeft = "1px solid #ccc"
        cth1L2.style.textAlign = "right"

        let cth2L2 =  document.createElement('th')
        cth2L2.innerHTML = `Valor Item`
        cth2L2.style.borderLeft = "1px solid #ccc"
        cth2L2.style.textAlign = "right"

        linha2CabecalhoTabelaFaturas.appendChild(cth1L2)
        linha2CabecalhoTabelaFaturas.appendChild(cth2L2)
    }
    // ilp = itemLicitacaoProducao
    itensLicitacaoProducaoFaturados = []
    for(ilp of controleFaturasContrato[2]){
        if(ilp.valor_total_item > 0){
            itensLicitacaoProducaoFaturados.push(ilp.id_item_licitacao_producao)
            let cth =  document.createElement('th')
            cth.innerHTML = `${ilp.numero_lote}.${ilp.numero_item} - ${ilp.especialidade}
            <br>${
                ilp.descricao_item
            }`
            cth.style.minWidth = "140px"
            cth.style.textAlign = "center"
            // definir borda da coluna
            cth.style.borderLeft = "1px solid #ccc"
            linhaCabecalhoTabelaFaturas.appendChild(cth)

            let cthL2 =  document.createElement('th')
            cthL2.innerHTML = `Valor Item`
            cthL2.style.borderLeft = "1px solid #ccc"
            cthL2.style.textAlign = "right"
            linhaCabecalhoTabelaFaturas.appendChild(cth)
            linha2CabecalhoTabelaFaturas.appendChild(cthL2)
        }
    }

    let cTTh = document.createElement('th')
    cTTh.innerHTML = `Total da Fatura`
    //alinhar verticalmente no meio
    cTTh.style.verticalAlign = "middle"
    cTTh.style.textAlign = "center"
    cTTh.rowSpan = 2
    cTTh.style.borderLeft = "1px solid #ccc"
    linhaCabecalhoTabelaFaturas.appendChild(cTTh)


    cabecalhoTabelaFaturas.appendChild(linhaCabecalhoTabelaFaturas)
    cabecalhoTabelaFaturas.appendChild(linha2CabecalhoTabelaFaturas)

    tabelaFaturas.appendChild(cabecalhoTabelaFaturas)

    let corpoTabelaFaturas = document.createElement('tbody')


    for(f of controleFaturasContrato[0]){
        let linhaFatura = document.createElement('tr')
        let c1Td = document.createElement('td')

        let aitemLoteLicitacao = document.createElement('a')
        aitemLoteLicitacao.innerHTML = `${f.numero_fatura} - ${f.mes_referencia}/${f.ano_referencia}`
        aitemLoteLicitacao.setAttribute('href', f.url)
        c1Td.appendChild(aitemLoteLicitacao)
        linhaFatura.appendChild(c1Td)

        for(fi of f.itens_fatura){
            let cTdh = document.createElement('td')
            cTdh.appendChild(document.createTextNode(
                `${segundosParaHora(fi.valor_total_item_fatura[1])}`))
            cTdh.style.textAlign = "right"
            linhaFatura.appendChild(cTdh)
            let cTdv = document.createElement('td')
            cTdv.appendChild(document.createTextNode(
                `${fi.valor_total_item_fatura[0].toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))
            cTdv.style.textAlign = "right"
            linhaFatura.appendChild(cTdv)
        }

        for(ifp of f.itens_producao_fatura){
            if(itensLicitacaoProducaoFaturados.includes(ifp.id_item_licitacao)){
            let cTdv = document.createElement('td')
            cTdv.appendChild(document.createTextNode(
                `${ifp.valor_total_item.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))
            cTdv.style.textAlign = "right"
            linhaFatura.appendChild(cTdv)
            }
        }

        let cTFd = document.createElement('td')
        cTFd.appendChild(document.createTextNode(
            `${f.valor_total_fatura.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))
        cTFd.style.textAlign = "right"
        linhaFatura.appendChild(cTFd)

        corpoTabelaFaturas.appendChild(linhaFatura)

    }
    tabelaFaturas.appendChild(corpoTabelaFaturas)

    tabelaFaturas.appendChild(criarRodapeFaturas(controleFaturasContrato[1], controleFaturasContrato[2]))

    linhaConteudoTabelaFaturas.appendChild(tabelaFaturas)
    linhaConteudoTabelaFaturas.appendChild(tabelaResumoFaturas)
    containerFaturas.appendChild(linhaConteudoTabelaFaturas)

    let itensProducaoFaturados = controleFaturasProducao.itens_licitacao
    let faturasProducao = controleFaturasProducao.faturas

    if(itensProducaoFaturados.length > 0){
        let tabelaFaturasProducao = criarContainerFaturasProducao(itensProducaoFaturados, faturasProducao)

        containerFaturas.appendChild(tabelaFaturasProducao)
    }

    return containerFaturas
}

function criarRodapeFaturas(itensLoteContrato, itensProducao){

    let tf = document.createElement('tfoot')

    let tr1 = document.createElement('tr')
    tr1.setAttribute('class', 'table-info')

    let tr12 = document.createElement('tr')
    tr12.setAttribute('class', 'table-info')

    let tr2 = document.createElement('tr')
    tr2.setAttribute('class', 'table-info')

    let th1 = document.createElement('th')
    th1.appendChild(document.createTextNode("Total Faturado: "))
    tr1.appendChild(th1)

    let th12 = document.createElement('th')
    th12.appendChild(document.createTextNode("Total Contratado: "))
    tr12.appendChild(th12)


    let th2 = document.createElement('th')
    th2.appendChild(document.createTextNode("Saldo:"))
    tr2.appendChild(th2)

    var totalContratado = 0
    var totalFaturado = 0

    for(ilc of itensLoteContrato){
        let td2 = document.createElement('td')
        td2.appendChild(document.createTextNode(
            `${segundosParaHora(ilc.valor_total_item[1])}`
        ))
        td2.style.textAlign = "right"
        let td3 = document.createElement('td')
        td3.appendChild(document.createTextNode(
            `${ilc.valor_total_item[0].toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`
        ))
        td3.style.textAlign = "right"
        let saldoHoras = ilc.quantidade*3600 - ilc.valor_total_item[1]
        let td4 = document.createElement('td')
        td4.appendChild(document.createTextNode(
            `${segundosParaHora(saldoHoras)}`
        ))

        td4.style.textAlign = "right"
        console.log("ILC total Faturas: ", ilc)
        let SaldoItem = ilc.quantidade*ilc.valor_un - ilc.valor_total_item[0]
        totalContratado += ilc.quantidade*ilc.valor_un

        let td5 = document.createElement('td')
        td5.appendChild(document.createTextNode(
            `${SaldoItem.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`
        ))
        td5.style.textAlign = "right"

        let td6 = document.createElement('td')
        td6.style.textAlign = "right"
        td6.appendChild(document.createTextNode(
            `${segundosParaHora(ilc.quantidade*3600)}`
        ))

        let td7 = document.createElement('td')
        td7.style.textAlign = "right"
        td7.appendChild(document.createTextNode(
            `${(ilc.quantidade*ilc.valor_un).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`
        ))

        totalFaturado += ilc.valor_total_item[0]
        tr1.appendChild(td2)
        tr1.appendChild(td3)
        tr12.appendChild(td6)
        tr12.appendChild(td7)
        tr2.appendChild(td4)
        tr2.appendChild(td5)

    }

    for(ilp of itensProducao){
        console.log("TF: ILP - ", ilp)
        if(ilp.valor_total_item > 0){
            let tdf1 = document.createElement('td')
            tdf1.appendChild(document.createTextNode(
                `${ilp.valor_total_item.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`
            ))
            tdf1.style.textAlign = "right"


            let SaldoItem = ilp.quantidade*ilp.valor_un - ilp.valor_total_item
            totalContratado += ilp.quantidade*ilp.valor_un

            let tdf2 = document.createElement('td')
            tdf2.appendChild(document.createTextNode(
                `${(ilp.quantidade*ilp.valor_un).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`
            ))
            tdf2.style.textAlign = "right"

            let tdf3 = document.createElement('td')
            tdf3.style.textAlign = "right"
            tdf3.appendChild(document.createTextNode(
                `${SaldoItem.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`
            ))

            tr1.appendChild(tdf1)
            tr12.appendChild(tdf2)
            tr2.appendChild(tdf3)

            totalFaturado += ilp.valor_total_item

        }
    }



    let th1T = document.createElement('th')
    th1T.style.textAlign = "right"
    th1T.appendChild(document.createTextNode(totalFaturado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })))

    let th12T = document.createElement('th')
    th12T.style.textAlign = "right"
    th12T.appendChild(document.createTextNode(totalContratado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })))

    let th2T = document.createElement('th')
    th2T.appendChild(document.createTextNode((totalContratado-totalFaturado).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })))
    th2T.style.textAlign = "right"

    tr1.appendChild(th1T)
    tr12.appendChild(th12T)
    tr2.appendChild(th2T)

    tf.appendChild(tr1)
    tf.appendChild(tr12)
    tf.appendChild(tr2)

    return tf
}


function criarLinhaTituloTabelaFaturas(tipoFatura){
    let linhaTabelaFaturas = document.createElement('div')
    linhaTabelaFaturas.setAttribute('class', 'row')
    linhaTabelaFaturas.setAttribute('id', 'linha-tabela-faturas')
    linhaTabelaFaturas.style.backgroundColor = "#abbcd3"
    linhaTabelaFaturas.style.height = '2rem'
    linhaTabelaFaturas.style.textAlign = 'center'


    let colunaTabelaFaturas = document.createElement('div')
    colunaTabelaFaturas.setAttribute('class', 'col')

    let linhaTituloTabelaFaturas = document.createElement('div')
    linhaTituloTabelaFaturas.setAttribute('class', 'row')
    linhaTituloTabelaFaturas.setAttribute('id', 'linha-titulo-tabela-faturas')

    let colunaTituloTabelaFaturas = document.createElement('div')
    colunaTituloTabelaFaturas.setAttribute('class', 'col')

    let tituloTabelaFaturas = document.createElement('strong')
    tituloTabelaFaturas.setAttribute('id', 'titulo-tabela-faturas')
    tituloTabelaFaturas.innerHTML = `Faturas (${tipoFatura})`

    colunaTituloTabelaFaturas.appendChild(tituloTabelaFaturas)
    linhaTituloTabelaFaturas.appendChild(colunaTituloTabelaFaturas)
    colunaTabelaFaturas.appendChild(linhaTituloTabelaFaturas)
    linhaTabelaFaturas.appendChild(colunaTabelaFaturas)

    return linhaTabelaFaturas

}

function criarContainerProfissionais(profissionaisHabilitados, editavel, itensHabilitaveis){
    let containerProfissionais = document.createElement('div')
    containerProfissionais.setAttribute('class', 'container-fluid')
    containerProfissionais.setAttribute('id', 'container-profissionais')

    let linhaProfissionais = document.createElement('div')
    linhaProfissionais.setAttribute('class', 'row')
    linhaProfissionais.setAttribute('id', 'linha-profissionais')
    linhaProfissionais.style.paddingTop = '1rem'
    linhaProfissionais.style.paddingBottom = '1rem'

    let colunaProfissionais = document.createElement('div')
    colunaProfissionais.setAttribute('class', 'col')

    let linhaBotaoHabilitarProfissionais = document.createElement('div')
    linhaBotaoHabilitarProfissionais.setAttribute('class', 'row')
    linhaBotaoHabilitarProfissionais.setAttribute('id', 'linha-titulo-tabela-profissionais')

    let colunaVaziaHabilitarProfissionais = document.createElement('div')
    colunaVaziaHabilitarProfissionais.setAttribute('class', 'col-8')

    let colunaBotaoHabilitarProfissionais = document.createElement('div')
    colunaBotaoHabilitarProfissionais.setAttribute('class', 'col-4')
    colunaBotaoHabilitarProfissionais.style.textAlign = 'right';

    let botaoHabilitar = document.createElement("div")
    botaoHabilitar.setAttribute('class', 'btn btn btn-primary btn-block')
    botaoHabilitar.appendChild(document.createTextNode("Habilitar Novo Profissional"))
    botaoHabilitar.setAttribute('onclick', `habilitarProfissional()`)
    botaoHabilitar.setAttribute("data-toggle", 'modal')
    botaoHabilitar.setAttribute("data-target", '#formulario-habilitar-profissional')


    if(editavel){
        colunaBotaoHabilitarProfissionais.appendChild(botaoHabilitar)
    }
    linhaBotaoHabilitarProfissionais.appendChild(colunaVaziaHabilitarProfissionais)
    linhaBotaoHabilitarProfissionais.appendChild(colunaBotaoHabilitarProfissionais)



    let linhaTituloTabelaProfissionais = document.createElement('div')
    linhaTituloTabelaProfissionais.setAttribute('class', 'row')
    linhaTituloTabelaProfissionais.setAttribute('id', 'linha-titulo-tabela-profissionais')

    let colunaTabelaTituloProfissionais = document.createElement('div')
    colunaTabelaTituloProfissionais.setAttribute('class', 'col-8')

    let titulo = document.createElement('strong')
    titulo.appendChild(document.createTextNode("Profissionais Habilitados:"))

    colunaTabelaTituloProfissionais.appendChild(titulo)
    linhaTituloTabelaProfissionais.appendChild(colunaTabelaTituloProfissionais)

    colunaProfissionais.appendChild(linhaTituloTabelaProfissionais)

    let linhaTabelaProfissionais = document.createElement('div')
    linhaTabelaProfissionais.setAttribute('class', 'row')
    linhaTabelaProfissionais.setAttribute('id', 'linha-tabela-profissionais')

    let colunaTabelaProfissionais = document.createElement('div')
    colunaTabelaProfissionais.setAttribute('class', 'col')

    let tabelaProfissionais = criarTabelaProfissionaisHabilitados(profissionaisHabilitados, editavel, itensHabilitaveis)

    colunaTabelaProfissionais.appendChild(tabelaProfissionais)

    linhaTabelaProfissionais.appendChild(colunaTabelaProfissionais)

    colunaProfissionais.appendChild(linhaBotaoHabilitarProfissionais)
    colunaProfissionais.appendChild(linhaTituloTabelaProfissionais)
    colunaProfissionais.appendChild(linhaTabelaProfissionais)

    linhaProfissionais.appendChild(colunaProfissionais)
    containerProfissionais.appendChild(linhaProfissionais)
    return containerProfissionais

}


function criarConteudoModalAdicionarLote(){

    var containerJanela = document.createElement('div');
    containerJanela.setAttribute('class', 'container-fluid');

    //un formulario para selecionar os lotes
    var formulario = criarFormularioBase("AdicionarLotes")

    var input3 = document.createElement('input');
    input3.setAttribute('type', 'hidden');
    input3.setAttribute('name', 'id_contrato');
    input3.setAttribute('value', id_contrato);

    formulario.appendChild(input3);

    for(lote of lotes_contrataveis){
        var linhaLote = document.createElement('div');
        linhaLote.setAttribute('class', 'form-row');

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
        checkboxLote.setAttribute('name', `id_lotes_contratados`);
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

function adicionarLote() {

    const idModal = 'janela-adicionar-lote';

    if(document.getElementById(idModal)){
        let modal = new bootstrap.Modal(document.getElementById(idModal))
        modal.show()
    }else{
        const tituloModal = "Adicionar Lotes ao Contrato"

        const conteudoModal = criarConteudoModalAdicionarLote()

        let janela_modal = criarModal(idModal, tituloModal, conteudoModal)

        document.body.appendChild(janela_modal)
        modal = new bootstrap.Modal(janela_modal)
        modal.show()

    }
}

function criarLinhaTabelaItens(vinculado, item, editavel, aditivoQuantidade, idLote){
    console.log("AQ: ", aditivoQuantidade, "Item: ", item)
    let linhaItemTabela = document.createElement('tr')
    if(vinculado){
        linhaItemTabela.setAttribute('id', `linhaItemTabelaVinculdo-${item.id}`)
        let td1 = document.createElement('td')
        td1.appendChild(document.createTextNode(`${item.str_numero_item}`))

        let td2 = document.createElement('td')
        td2.appendChild(document.createTextNode(`${item.descricao_item}`))
        let td3 = document.createElement('td')
        td3.appendChild(document.createTextNode(`${item.unidade_medida}`))
        let td4 = document.createElement('td')
        if(aditivoQuantidade){if(aditivoQuantidade.editavel){
            elQuantidade = criarInputQuantidadeAditivada(item.id, item.quantidade_contratada, null)
        }else{elQuantidade = document.createTextNode(`${item.quantidade_contratada}`)}}else{
            elQuantidade = document.createTextNode(`${item.quantidade_contratada}`)
        }
        td4.appendChild(elQuantidade)
        let td5 = document.createElement('td')
        td5.setAttribute(`data-valorUnitarioItem`, item.valor_item)
        td5.setAttribute(`data-idValorUnitarioItem`, item.id)
        td5.appendChild(document.createTextNode(`${item.valor_item.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))

        let td6 = document.createElement('td')
        td6.setAttribute('id', 'tdValorTotalItem')
        let valorTotal = item.quantidade_contratada * item.valor_item
        td6.setAttribute(`data-valorTotalItem`, valorTotal)
        td6.setAttribute(`data-idValorTotalItem`, item.id)
        td6.setAttribute(`data-idLoteValorTotalItem`, idLote)
        td6.appendChild(document.createTextNode(`${valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))

        var td7 = document.createElement('td')

        if(statusContrato === "cadastro"){
            let iconeExcluir = document.createElement('i')
            iconeExcluir.setAttribute('class', 'fas fa-trash-alt')
            iconeExcluir.style.cursor = "pointer"
            iconeExcluir.style.color = "red"
            iconeExcluir.setAttribute('onclick', `excluirItemLoteContrato(${item.id})`)
            td7.appendChild(iconeExcluir)
        }else if(aditivoQuantidade){if(aditivoQuantidade.editavel){
            let iconeAtualizarQuantidade = criarIconeAtualizarQuantidade(
                item.id, aditivoQuantidade.id, null)
            td7.appendChild(iconeAtualizarQuantidade)}}

        linhaItemTabela.appendChild(td1)
        linhaItemTabela.appendChild(td2)
        linhaItemTabela.appendChild(td3)
        linhaItemTabela.appendChild(td4)
        linhaItemTabela.appendChild(td5)
        linhaItemTabela.appendChild(td6)
        linhaItemTabela.appendChild(td7)

        if(!editavel){
            if(aditivoQuantidade){if(!aditivoQuantidade.editavel){
                adicionarTotalFaturadoLinhaTabela(linhaItemTabela, item.valor_item, item.quantidade_contratada, item.valor_total_faturado[0])
            }}else{
                adicionarTotalFaturadoLinhaTabela(linhaItemTabela, item.valor_item, item.quantidade_contratada, item.valor_total_faturado[0])
            }
        }

    }else{
        linhaItemTabela.setAttribute('id', `linhaItemTabelaVinculavel-${item.id}`)
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
        inputQuantidade.setAttribute('id', `inputQuantidadeItemLote-${item.id}`)
        inputQuantidade.setAttribute('onchange', `calcularValorTotalItemLote(${item.id})`)
        inputQuantidade.setAttribute('value', `${item.quantidade_licitada}`)
        td4.appendChild(inputQuantidade)
        let td5 = document.createElement('td')
        let inputValor = document.createElement('input')
        inputValor.setAttribute('type', 'number')
        inputValor.setAttribute('step', '0.01')
        inputValor.setAttribute('class', 'form-control')
        inputValor.style.minWidth = "6rem"
        inputValor.setAttribute('id', `inputValorItemLote-${item.id}`)
        inputValor.setAttribute('onchange', `calcularValorTotalItemLote(${item.id})`)
        inputValor.setAttribute('value', `${item.valor_licitado}`)
        td5.appendChild(inputValor)
        let td6 = document.createElement('td')
        let inputValorTotal = document.createElement('input')
        inputValorTotal.setAttribute('step', '0.01')
        inputValorTotal.setAttribute('class', 'form-control')
        inputValorTotal.style.minWidth = "9rem"
        inputValorTotal.setAttribute('id', `inputValorTotalItemLote-${item.id}`)
        inputValorTotal.disabled = true

        let valorTotal = item.valor_licitado * item.quantidade_licitada
        inputValorTotal.value = valorTotal.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
        td6.appendChild(inputValorTotal)

        let td7 = document.createElement('td')

        let iconeSalvar = document.createElement('i')
        iconeSalvar.setAttribute('class', 'fas fa-plus')
        iconeSalvar.style.cursor = "pointer"
        iconeSalvar.style.color = "green"
        iconeSalvar.setAttribute('onclick', `salvarItemLoteContrato(${item.id}); this.removeAttribute('onclick')`)
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

function recarregarPagina(response){
    if(response.status === 'success'){
        window.location.reload()
    }else{
        alert("Erro ao processar a requisicao")
    }

}

function calcularValorTotalItemLote(idItemLote){
    let inputQuantidade = document.getElementById(`inputQuantidadeItemLote-${idItemLote}`)
    let inputValor = document.getElementById(`inputValorItemLote-${idItemLote}`)
    let inputValorTotal = document.getElementById(`inputValorTotalItemLote-${idItemLote}`)

    let quantidade = inputQuantidade.value
    let valor = inputValor.value
    let valorTotal = quantidade * valor

    inputValorTotal.value = valorTotal.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
}

function finalizarCadastroContrato(){
    let url = window.location.href

    let dados = criarFormdata("finalizar_cadastro_contrato")
    dados.append('id-contrato-finalizar-cadastro', id_contrato)

    enviarFormData(dados, recarregarPagina)

}

function apagarContrato() {

    const idModal = 'formulario-apagar-contrato';

    if(document.getElementById(idModal)){
        let modal = new bootstrap.Modal(document.getElementById(idModal))
        modal.show()
    }else{
        const tituloModal = "Deseja Realmente apagar o contrato?"

        const conteudoModal = criarConteudoModalApagarContrato()

        let janela_modal = criarModal(idModal, tituloModal, conteudoModal)

        document.body.appendChild(janela_modal)
        modal = new bootstrap.Modal(janela_modal)
        modal.show()

    }
}

function criarConteudoModalApagarContrato(){
     var containerJanela = document.createElement('div');
    containerJanela.setAttribute('class', 'container-fluid');

    var formulario = criarFormularioBase("apagar_contrato")

    var inputIdContrato = document.createElement('input');
    inputIdContrato.setAttribute('name', 'id-contrato');
    inputIdContrato.setAttribute('id', 'id-contrato');
    inputIdContrato.setAttribute('value', id_contrato);
    inputIdContrato.setAttribute('type', 'hidden');

    formulario.appendChild(inputIdContrato)

    let submitFormulario = document.createElement('button');
    submitFormulario.setAttribute('type', 'submit');
    submitFormulario.setAttribute('class', 'btn btn-danger');
    submitFormulario.appendChild(document.createTextNode('Apagar Contrato'));
    formulario.appendChild(submitFormulario);

    let paragrafo = document.createElement('p')
    paragrafo.appendChild(document.createTextNode("essa ação não poderá ser desfeita e todos os dados relacionados ao contrato serção perdidos."))

    containerJanela.append(paragrafo, formulario)
    return containerJanela
}


function rescindirContrato(){

    const idModal = 'formulario-rescindir-contrato';

    if(document.getElementById(idModal)){
        let modal = new bootstrap.Modal(document.getElementById(idModal))
        modal.show()
    }else{
        const tituloModal = "Informe o motivo da rescisão:"

        const conteudoModal = criarConteudoModalRescindirContrato()

        let janela_modal = criarModal(idModal, tituloModal, conteudoModal)

        document.body.appendChild(janela_modal)
        modal = new bootstrap.Modal(janela_modal)
        modal.show()

    }
}

function criarConteudoModalRescindirContrato(){

     var containerJanela = document.createElement('div');
    containerJanela.setAttribute('class', 'container-fluid');

    var formulario = criarFormularioBase("rescindir_contrato")

    let grupoDadosColaborador = document.createElement('div');
    grupoDadosColaborador.setAttribute('class', 'form-group');

    var inputIdContrato = document.createElement('input');
    inputIdContrato.setAttribute('name', 'id-contrato');
    inputIdContrato.setAttribute('id', 'id-contrato');
    inputIdContrato.setAttribute('value', id_contrato);
    inputIdContrato.setAttribute('type', 'hidden');

    var inputMotivoRescisao = document.createElement('textarea');
    inputMotivoRescisao.setAttribute('id', 'id_input_motivo_recisao');
    inputMotivoRescisao.setAttribute('name', 'input_motivo_rescisao');
    inputMotivoRescisao.setAttribute('rows', '3');
    inputMotivoRescisao.setAttribute('class', 'form-control');

    grupoDadosColaborador.appendChild(inputIdContrato);

    grupoDadosColaborador.appendChild(inputMotivoRescisao);

    formulario.appendChild(grupoDadosColaborador);
    let submitFormulario = document.createElement('button');
    //submitFormulario.setAttribute('onclick', 'enviarRescisao();');
    submitFormulario.setAttribute('type', 'submit');
    submitFormulario.setAttribute('class', 'btn btn-danger');
    submitFormulario.appendChild(document.createTextNode('Confirmar Rescisão'));
    submitFormulario.style.marginTop = "15px"
    formulario.appendChild(submitFormulario);

    containerJanela.appendChild(formulario)

    return containerJanela

}

function aditivarContrato(){

    const idModal = 'janela-aditivar-contrato';

    if(document.getElementById(idModal)){
        let modal = new bootstrap.Modal(document.getElementById(idModal))
        modal.show()
    }else{
        const tituloModal = "Informações do Aditivo:"

        const conteudoModal = criarConteudoModalAditivarContrato()

        let janela_modal = criarModal(idModal, tituloModal, conteudoModal)

        document.body.appendChild(janela_modal)
        modal = new bootstrap.Modal(janela_modal)
        modal.show()

    }
}

function criarConteudoModalAditivarContrato(){

    let containerJanela = document.createElement('div');
    containerJanela.setAttribute('class', 'container-fluid');

    let formulario = criarFormularioBase("aditivar_contrato")

    let inputIdContrato = document.createElement('input');
    inputIdContrato.setAttribute('name', 'id-contrato');
    inputIdContrato.setAttribute('id', 'id-contrato');
    inputIdContrato.setAttribute('value', id_contrato);
    inputIdContrato.setAttribute('type', 'hidden');

    formulario.append(inputIdContrato);

    let linhaAditivoQuantidade = document.createElement('div');
    linhaAditivoQuantidade.setAttribute('class', 'form-row');

    let containerSwitch = document.createElement('div')
    containerSwitch.setAttribute('class', 'container-fluid')

    let switchAditivoQuantidade = document.createElement("div")
    switchAditivoQuantidade.setAttribute('class', 'custom-control custom-switch')
    switchAditivoQuantidade.setAttribute('id', `div-switch-aditivo-quantidade`)

    let inputSwitchAditivoQuantidade = document.createElement('input')
    inputSwitchAditivoQuantidade.setAttribute('class', 'custom-control-input')
    inputSwitchAditivoQuantidade.setAttribute('type', 'checkbox')
    inputSwitchAditivoQuantidade.setAttribute('id', `switch-aditivo-quantidade`)
    inputSwitchAditivoQuantidade.setAttribute("onchange", `alternarAditivarSuprimirQuantidade(this)`)

    let lableinputSwitchAditivoQuantidade = document.createElement('label')
    lableinputSwitchAditivoQuantidade.appendChild(document.createTextNode('Aditivar/Suprimir Quantidade (Não Altera a Vigência)'))
    lableinputSwitchAditivoQuantidade.setAttribute('class', 'custom-control-label')
    lableinputSwitchAditivoQuantidade.setAttribute('for', `switch-aditivo-quantidade`)

    switchAditivoQuantidade.appendChild(inputSwitchAditivoQuantidade)
    switchAditivoQuantidade.appendChild(lableinputSwitchAditivoQuantidade)
    containerSwitch.appendChild(switchAditivoQuantidade)

    linhaAditivoQuantidade.appendChild(containerSwitch)

    let linhaNumeroAditivo = document.createElement('div');
    linhaNumeroAditivo.setAttribute('class', 'row');

    let colunaNumeroAditivo = document.createElement('div');
    colunaNumeroAditivo.setAttribute('class', 'col');

    let colunaTipoAditivo = document.createElement('div');
    colunaTipoAditivo.setAttribute('class', 'col');

    let divNumeroAditivo = document.createElement('div');
    divNumeroAditivo.setAttribute('class', 'container-fluid');

    let lableNumeroAditivo = document.createElement('label');
    lableNumeroAditivo.setAttribute('class', 'form-check-label');
    lableNumeroAditivo.appendChild(document.createTextNode(`Número do aditivo: `));

    let inputNumeroAditivo = document.createElement('input');
    inputNumeroAditivo.setAttribute('type', 'number');
    inputNumeroAditivo.setAttribute('class', 'form-control');
    inputNumeroAditivo.setAttribute('name', 'numero_aditivo');
    inputNumeroAditivo.setAttribute('placeholder', 'Número do aditivo');
    inputNumeroAditivo.setAttribute('required', 'required');

    let divTipoAditivo = document.createElement('div');
    divTipoAditivo.setAttribute('class', 'container-fluid');

    // um select para selecionar o tipo do aditivo
    let lableTipoAditivo = document.createElement('label');
    lableTipoAditivo.setAttribute('class', 'form-check-label');
    lableTipoAditivo.appendChild(document.createTextNode(`Tipo do aditivo: `));

    let selectTipoAditivo = document.createElement('select');
    selectTipoAditivo.setAttribute('class', 'form-control');
    selectTipoAditivo.setAttribute('name', 'tipo_aditivo');
    selectTipoAditivo.setAttribute('required', 'required');

    for(ta of tiposAditivo){
        let optionTipoAditivo = document.createElement('option');
        optionTipoAditivo.setAttribute('value', ta);
        optionTipoAditivo.appendChild(document.createTextNode(ta));
        selectTipoAditivo.appendChild(optionTipoAditivo);

    }

    let linhaLableVigenciaAditivo = document.createElement('div');
    linhaLableVigenciaAditivo.setAttribute('class', 'row');
    linhaLableVigenciaAditivo.setAttribute('id', 'linha-lable-vigencia-aditivo')

    let colunaLableVigenciaAditivo = document.createElement('div');
    colunaLableVigenciaAditivo.setAttribute('class', 'col');

    colunaLableVigenciaAditivo.appendChild(document.createTextNode(`Vigência do aditivo: `));

    linhaLableVigenciaAditivo.appendChild(colunaLableVigenciaAditivo);

    let linhaVigenciaAditivo = document.createElement('div');
    linhaVigenciaAditivo.setAttribute('class', 'row');
    linhaVigenciaAditivo.setAttribute('id', 'linha-input-vigencia-aditivo')

    let colunaInicioVigenciaAditivo = document.createElement('div');
    colunaInicioVigenciaAditivo.setAttribute('class', 'col');

    let inputInicioVigenciaAditivo = document.createElement('input');
    inputInicioVigenciaAditivo.setAttribute('type', 'date');
    inputInicioVigenciaAditivo.setAttribute('class', 'form-control');
    inputInicioVigenciaAditivo.setAttribute('name', 'inicio_vigencia');

    let colunaFimVigenciaAditivo = document.createElement('div');
    colunaFimVigenciaAditivo.setAttribute('class', 'col');

    let inputFimVigenciaAditivo = document.createElement('input');
    inputFimVigenciaAditivo.setAttribute('type', 'date');
    inputFimVigenciaAditivo.setAttribute('class', 'form-control');
    inputFimVigenciaAditivo.setAttribute('name', 'fim_vigencia');

    let dataInicioVigenciaAditivo = new Date(fimVigencia);
    dataInicioVigenciaAditivo.setDate(dataInicioVigenciaAditivo.getDate() + 1);

    let dataFimVigenciaAditivo = new Date(fimVigencia);
    dataFimVigenciaAditivo.setDate(dataFimVigenciaAditivo.getDate() + 365);

    inputInicioVigenciaAditivo.value = dataInicioVigenciaAditivo.toISOString().substring(0, 10);
    inputFimVigenciaAditivo.value = dataFimVigenciaAditivo.toISOString().substring(0, 10);

    colunaInicioVigenciaAditivo.appendChild(inputInicioVigenciaAditivo);
    colunaFimVigenciaAditivo.appendChild(inputFimVigenciaAditivo);

    linhaVigenciaAditivo.appendChild(colunaInicioVigenciaAditivo);
    linhaVigenciaAditivo.appendChild(colunaFimVigenciaAditivo);

    divTipoAditivo.appendChild(lableTipoAditivo);
    divTipoAditivo.appendChild(selectTipoAditivo);

    divNumeroAditivo.appendChild(lableNumeroAditivo);
    divNumeroAditivo.appendChild(inputNumeroAditivo);

    colunaNumeroAditivo.appendChild(divNumeroAditivo);
    colunaTipoAditivo.appendChild(divTipoAditivo);

    linhaNumeroAditivo.appendChild(colunaNumeroAditivo);
    linhaNumeroAditivo.appendChild(colunaTipoAditivo);

    formulario.appendChild(linhaAditivoQuantidade)
    formulario.appendChild(linhaNumeroAditivo);
    formulario.appendChild(linhaLableVigenciaAditivo);
    formulario.appendChild(linhaVigenciaAditivo);

    let submitForm = document.createElement('button');
    submitForm.setAttribute('type', 'submit');
    submitForm.setAttribute('class', 'btn btn-primary');
    submitForm.appendChild(document.createTextNode('Aditivar Contrato'));

    formulario.appendChild(document.createElement('br'));
    formulario.appendChild(submitForm);

    containerJanela.appendChild(formulario);



    containerJanela.appendChild(formulario)

    return containerJanela

}

function alternarAditivarSuprimirQuantidade(e){
    console.log(e)
    e = e.parentNode.parentNode.parentNode.parentNode.parentNode
    console.log("E", e)
    let switchAditivoQualtidade = e.querySelector("#switch-aditivo-quantidade")
    let linhaVigenciaAditivo = e.querySelector('#linha-input-vigencia-aditivo')
    let linhaLableVigenciaAditivo = e.querySelector('#linha-lable-vigencia-aditivo')
    let inputTipoFormulario = e.querySelector('#id-aditivar_contrato')
    let valorSwitch = switchAditivoQualtidade.checked
    if(valorSwitch){
        linhaVigenciaAditivo.hidden = true
        linhaLableVigenciaAditivo.hidden=true
        inputTipoFormulario.value="aditivar-suprimir-quantidade-contratada"
    }else{
        linhaVigenciaAditivo.hidden = false
        linhaLableVigenciaAditivo.hidden=false
        inputTipoFormulario.value="aditivar_contrato"}
}

function cancelarAditivoQuantidade(e) {
    console.log(e)
    let idAditivo = e.getAttribute('data-idaditivoquantidade')
    console.log(idAditivo)


    let dados = criarFormdata("cancelar_aditivo_quantidade")

    dados.append('id-aditivo-quantidade', idAditivo)
    dados.append('id-contrato', id_contrato)

    enviarFormData(dados, recarregarPagina)
}

function adicionarTotalFaturadoLinhaTabela(linhaItemTabela, valorUnitario, quantidade, valorTotalFaturado ){
    console.log('linhaItemTabela', 'valorUnitario', 'quantidade', 'valorTotalFaturado')
    console.log(linhaItemTabela, valorUnitario, quantidade, valorTotalFaturado)
    let td8 = document.createElement('td')
    td8.setAttribute('id', 'tdValorFaturadoItem')
    td8.setAttribute(`data-ValorFaturadoItem`, valorTotalFaturado)
    td8.appendChild(document.createTextNode(`${valorTotalFaturado.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))
    let td9 = document.createElement('td')
    let saldo = (quantidade * valorUnitario) - valorTotalFaturado
    td9.setAttribute(`data-saldoTotalItem`, `${saldo}`)
    td9.appendChild(document.createTextNode(`${saldo.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}`))

    linhaItemTabela.appendChild(td8)
    linhaItemTabela.appendChild(td9)

}
function processarValorTotalLote(idLote){
    console.log("ID Lote: ", idLote)
    let valorLote = calcularValorTotalLoteContratado(idLote)
    console.log("Valor Total: ", valorLote)
    let tdValorTotalLote = document.querySelector(`td[data-idLoteValorTotalContratadoLote="${idLote}"]`)
    console.log(tdValorTotalLote)
    console.log('FS: ', tdValorTotalLote.firstChild)
    tdValorTotalLote.removeChild(tdValorTotalLote.firstChild)
    tdValorTotalLote.appendChild(document.createTextNode(valorLote.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })))
}

function criarItensVisualizar(){
    let navVisualizacoes = document.getElementById("nav-visualizacoes");
    for(v of visualizacoes){

        let item = document.createElement("li");
        item.className = "nav-item";
        let link = document.createElement("a");
        link.style.cursor = 'pointer'
        link.id = `link-${v.tipo}-${v.id}`;
        link.setAttribute('data-tipo', v.tipo);
        link.setAttribute('data-id', v.id);
        link.setAttribute('onclick', `visualizarLotes('${v.tipo}', '${v.id}')`);

        if(v.ativo){
            link.className = "pill-view nav-link active disabled";
            criarTabelasLotes(v.tipo, v.id);
        }else{
            link.className = "pill-view nav-link";
        }
        link.innerHTML = v.descricao;
        item.appendChild(link);
        navVisualizacoes.appendChild(item);
    }
}

function salvarItemLoteContrato(idItemLoteLicitacao){
    let inputQuantidade = document.getElementById(`inputQuantidadeItemLote-${idItemLoteLicitacao}`)
    let inputValor = document.getElementById(`inputValorItemLote-${idItemLoteLicitacao}`)
    let inputValorTotal = document.getElementById(`inputValorTotalItemLote-${idItemLoteLicitacao}`)
    let quantidade = inputQuantidade.value
    let valor = inputValor.value

    let dados = criarFormdata("adicionar-item-lote-contratado");
    dados.append('id-item-lote-licitacao', idItemLoteLicitacao)
    dados.append('quantidade-contratada', quantidade)
    dados.append('valor-contratado', valor)
    dados.append('id-contrato', id_contrato)
    enviarFormData(dados, processarSalvarItemLoteContrato)
}

function processarSalvarItemLoteContrato(response){
    if(response.status === 'success'){
        let tabelaAdicionarNovaLinha = document.getElementById(`ItensTabelaLote-${response.idLoteContrato}`)
        let linhaItemTabela = criarLinhaTabelaItens(true, response.itemContratado, true, null, response.idLoteContrato) //(response.itemContratado, response.idLoteContrato)
        let linhaRemover = tabelaAdicionarNovaLinha.querySelector(`#linhaItemTabelaVinculavel-${response.idItemLoteLicitacao}`)
        tabelaAdicionarNovaLinha.replaceChild(linhaItemTabela, linhaRemover)
    }else{
        alert("Erro ao processar a requisicao")
    }




}

function excluirItemLoteContrato(idItemLoteContrato){

    let dados = criarFormdata("excluir-item-lote-contratado")
    dados.append('id-item-lote-contratado', idItemLoteContrato)
    enviarFormData(dados, recarregarPagina)

}

function processarExcluirItemLoteContrato(response){
    if(response.status === 'success'){
        let tabelaAdicionarNovaLinha = document.getElementById(`ItensTabelaLote-${response.idLoteContrato}`)
        let linhaItemTabela = criarLinhaTabelaItens(false, response.itemContratado, true, null, response.idLoteContrato) //(response.itemContratado, response.idLoteContrato)
        let linhaRemover = tabelaAdicionarNovaLinha.querySelector(`#linhaItemTabelaVinculdo-${response.idLoteContrato.id}`)
        tabelaAdicionarNovaLinha.replaceChild(linhaItemTabela, linhaRemover)
    }else{
        alert("Erro ao excluir o item")
    }
}

function excluirLoteContratado(idLoteContrato){
    if(confirm('Deseja realmente excluir este lote?')){
        let dados = criarFormdata("excluir-lote-contratado")
        dados.append('id-lote-contratado', idLoteContrato)
        enviarFormData(dados, recarregarPagina)
    }
}



