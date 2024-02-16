
function criarNavTodosColaboradores(ativa){
    let aTodos = document.createElement('a')
    aTodos.className = `nav-link ${ativa}`
    aTodos.href = urlColaboradores
    aTodos.innerHTML = "Todos"
    return aTodos
}

function criarNavUnidadeSetoresColaboradores(unidades){
    let navbarLight = document.createElement('nav')
    navbarLight.className = "navbar navbar-light"

    let ulNavbar = document.createElement('ul')
    ulNavbar.className = "navbar-nav"
    ulNavbar.appendChild(criarNavTodosColaboradores("active"))
    for(let unidade of unidades){
        let aUnidade = document.createElement('a')
        console.log(unidade.ativa)
        if(unidade.ativa){
            aUnidade.className = "nav-link active"
        }else{
            aUnidade.className = "nav-link"
        }
        aUnidade.href = `${urlColaboradores}unidade/${unidade.slug}`
        aUnidade.innerHTML = unidade.nome_unidade
        ulNavbar.appendChild(aUnidade)
        let setores = unidade.setores_unidade
        console.log(unidade.slug)
        let navSetors = criarNavSetoresColaboradores(setores, unidade.slug)
        ulNavbar.append(navSetors)
    }

    navbarLight.appendChild(ulNavbar)

    return navbarLight
}

function criarNavSetoresColaboradores(setores, slug_unidade){
    let divContainer = document.createElement('div')
    divContainer.className = "container-fluid"

    let navbarLight = document.createElement('nav')
    navbarLight.className = "navbar navbar-light"

    let ulNavbar = document.createElement('ul')
    ulNavbar.className = "navbar-nav"
    for(let setor of setores){
        let liSetor = document.createElement('li')
        liSetor.className = "nav-item"

        let aSetor = document.createElement('a')
        console.log(setor)
        console.log(setor['setor_ativo'], "SA")
        if (setor['setor_ativo'] === true){
            aSetor.className = "nav-link active"
        }else{
            aSetor.className = "nav-link"
        }
        aSetor.innerHTML = setor.nome_setor
        aSetor.href = `${urlColaboradores}unidade/${slug_unidade}/${setor.slug}`


        liSetor.appendChild(aSetor)
        ulNavbar.appendChild(liSetor)
        if(setor.setores_setor){
            let navSetoresSetor = criarNavSetoresColaboradores(setor.setores_setor, slug_unidade)
            ulNavbar.appendChild(navSetoresSetor)
        }
    }
    navbarLight.appendChild(ulNavbar)

    divContainer.appendChild(navbarLight)

    return divContainer
}


function buscarPessoas(unidade, setor){
    const cpf = document.getElementById("buscar-cpf").value
    const nome = document.getElementById('buscar-nome').value

    const form = criarFormdata("buscar-pessoas")
    form.append('unidade', unidade)
    form.append('setor', setor)
    form.append("cpf", cpf)
    form.append('nome', nome)
    enviarFormData(form, processarBuscaPessoas)
}

function criarTabelaTodosColaboradores(colaboradores){
    const tBody = document.getElementById("dados-pessoas")
    tBody.innerHTML = ""
    for(c of colaboradores){
        tBody.appendChild(criarLinhaColaborador(c))
    }
}

function processarBuscaPessoas(response){
    console.log(response)
    criarTabelaTodosColaboradores(response.funcionarios)
}

function criarLinhaColaborador(c){
    urlColaborador = `${urlColaboradores}colaborador/${c.slug}`
    let linhaColaborador = document.createElement('tr')
    let celulaCPF = document.createElement('td')
    let aCPF = document.createElement('a')
    aCPF.href = urlColaborador
    aCPF.appendChild(document.createTextNode(c.cpf))
    celulaCPF.appendChild(aCPF)

    let celulaNome = document.createElement('td')

    let aNome = document.createElement('a')
    aNome.href = urlColaborador
    aNome.appendChild(document.createTextNode(c.nome))
    celulaNome.appendChild(aNome)

    let celulaVinculo = document.createElement("td")
    if(c.vinculos_funcionario){
        for(v of c.vinculos_funcionario){
            let linhaFuncao = document.createElement('tr')
            let funcao = document.createElement('td')
            funcao.appendChild(document.createTextNode(`${v.funcao} - ${v.tipo_vinculo}`))
            linhaFuncao.appendChild(funcao)
            celulaVinculo.appendChild(linhaFuncao)
        }
    }

    linhaColaborador.appendChild(celulaCPF)
    linhaColaborador.appendChild(celulaNome)
    linhaColaborador.appendChild(celulaVinculo)

    return linhaColaborador
}