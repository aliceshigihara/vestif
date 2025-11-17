const instituicaoSelect = document.getElementById('instituicao');
const campusSelect = document.getElementById('campus');
const cursoSelect = document.getElementById('curso');
const detalhesDiv = document.getElementById('detalhes');

// preencher o select
function preencherSelect(select, dados) {
  select.innerHTML = '<option value="">Selecione</option>';
  dados.forEach(item => {
    const option = document.createElement('option');
    option.value = item;
    option.textContent = item;
    select.appendChild(option);
  });
  select.disabled = false;
}

// lista das instituicoes
function getInstituicoes() {
  return dados.map(obj => Object.keys(obj)[0]);
}

// campi da instituicao referente
function getCampi(instituicao) {
  const obj = dados.find(o => Object.keys(o)[0] === instituicao);
  if (!obj) return [];
  return Object.keys(obj[instituicao]);
}

// curso dos dois
function getCursos(instituicao, campus) {
  const obj = dados.find(o => Object.keys(o)[0] === instituicao);
  if (!obj) return [];
  return obj[instituicao][campus].map(c => c.curso);
}

// detalhes do curso
function getDetalhes(instituicao, campus, curso) {
  const obj = dados.find(o => Object.keys(o)[0] === instituicao);
  if (!obj) return null;
  return obj[instituicao][campus].find(c => c.curso === curso);
}

// inicializa a instituicao
preencherSelect(instituicaoSelect, getInstituicoes());

// momento em q escolhe a instituicao
instituicaoSelect.addEventListener('change', () => {
  const instituicao = instituicaoSelect.value;
  campusSelect.disabled = true;
  cursoSelect.disabled = true;
  detalhesDiv.innerHTML = '';

  if (!instituicao) return;

  preencherSelect(campusSelect, getCampi(instituicao));
});

// quando for escolher campus
campusSelect.addEventListener('change', () => {
  const instituicao = instituicaoSelect.value;
  const campus = campusSelect.value;
  cursoSelect.disabled = true;
  detalhesDiv.innerHTML = '';

  if (!campus) return;

  preencherSelect(cursoSelect, getCursos(instituicao, campus));
});

// quando for escolher o curso
cursoSelect.addEventListener('change', () => {
  const instituicao = instituicaoSelect.value;
  const campus = campusSelect.value;
  const curso = cursoSelect.value;
  detalhesDiv.innerHTML = '';

  if (!curso) return;

  const detalhe = getDetalhes(instituicao, campus, curso);

  // mostra os detalhes com html
  if (detalhe) {
    detalhesDiv.innerHTML = `
      <h3>Detalhes do Curso:</h3>
      <p><strong>Curso:</strong> ${detalhe.curso}</p>
      <p><strong>Turno:</strong> ${detalhe.turno}</p>
      <p><strong>Nota de Corte:</strong> ${detalhe.notaCorte}</p>
      <p><strong>Vagas:</strong> ${detalhe.vagas}</p>
    `;
  } else {
    detalhesDiv.textContent = 'Nenhuma informação encontrada.';
  }
});