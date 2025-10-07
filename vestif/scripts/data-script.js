const instituicaoSelect = document.getElementById('instituicao');
const campusSelect = document.getElementById('campus');
const cursoSelect = document.getElementById('curso');
const detalhesDiv = document.getElementById('detalhes');

// Função para preencher <select>
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

// 🔹 Obter lista de instituições
function getInstituicoes() {
  return dados.map(obj => Object.keys(obj)[0]);
}

// 🔹 Obter lista de campi de uma instituição
function getCampi(instituicao) {
  const obj = dados.find(o => Object.keys(o)[0] === instituicao);
  if (!obj) return [];
  return Object.keys(obj[instituicao]);
}

// 🔹 Obter lista de cursos de uma instituição e campus
function getCursos(instituicao, campus) {
  const obj = dados.find(o => Object.keys(o)[0] === instituicao);
  if (!obj) return [];
  return obj[instituicao][campus].map(c => c.curso);
}

// 🔹 Obter detalhes de um curso específico
function getDetalhes(instituicao, campus, curso) {
  const obj = dados.find(o => Object.keys(o)[0] === instituicao);
  if (!obj) return null;
  return obj[instituicao][campus].find(c => c.curso === curso);
}

// Inicializar instituições
preencherSelect(instituicaoSelect, getInstituicoes());

// Quando escolher instituição
instituicaoSelect.addEventListener('change', () => {
  const instituicao = instituicaoSelect.value;
  campusSelect.disabled = true;
  cursoSelect.disabled = true;
  detalhesDiv.innerHTML = '';

  if (!instituicao) return;

  preencherSelect(campusSelect, getCampi(instituicao));
});

// Quando escolher campus
campusSelect.addEventListener('change', () => {
  const instituicao = instituicaoSelect.value;
  const campus = campusSelect.value;
  cursoSelect.disabled = true;
  detalhesDiv.innerHTML = '';

  if (!campus) return;

  preencherSelect(cursoSelect, getCursos(instituicao, campus));
});

// Quando escolher curso
cursoSelect.addEventListener('change', () => {
  const instituicao = instituicaoSelect.value;
  const campus = campusSelect.value;
  const curso = cursoSelect.value;
  detalhesDiv.innerHTML = '';

  if (!curso) return;

  const detalhe = getDetalhes(instituicao, campus, curso);

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