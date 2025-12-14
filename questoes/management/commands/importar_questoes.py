import csv
from django.core.management.base import BaseCommand
from questoes.models import Questao, Prova

class Command(BaseCommand):
    help = 'Importa questões de um arquivo CSV (Com Alternativas)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Caminho do arquivo CSV')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        self.stdout.write(f"--- Lendo arquivo: {csv_file} ---")

        # 1. Cria a Prova Padrão
        prova, _ = Prova.objects.get_or_create(titulo='Vestibular UFSC', ano=2025)

        # 2. Tenta abrir detectando encoding
        try:
            file = open(csv_file, 'r', encoding='utf-8-sig')
            content = file.read()
        except UnicodeDecodeError:
            file = open(csv_file, 'r', encoding='latin-1')
            content = file.read()
        
        file.seek(0)

        # 3. Descobre o separador
        if ';' in file.readline():
            delimiter = ';'
        else:
            delimiter = ','
        
        file.seek(0)
        
        reader = csv.DictReader(file, delimiter=delimiter)
        
        # Normaliza cabeçalhos (tudo minúsculo)
        reader.fieldnames = [nome.strip().lower().replace('"', '') for nome in reader.fieldnames]
        print(f"Colunas encontradas: {reader.fieldnames}")

        count = 0
        for row in reader:
            # Limpa chaves da linha
            row = {k.strip().lower().replace('"', ''): v for k, v in row.items() if k}
            
            # --- Tenta encontrar as colunas das alternativas ---
            # Procura por '01', 'prop01', 'texto01', etc.
            def achar_texto(codigos_possiveis):
                for cod in codigos_possiveis:
                    if cod in row and row[cod]:
                        return row[cod]
                return None # Retorna None se não achar nada

            try:
                Questao.objects.create(
                    prova=prova,
                    numero=int(row['numero']),
                    disciplina=row.get('disciplina', 'Geral'),
                    enunciado=row.get('enunciado', 'Sem enunciado'),
                    resposta=row.get('gabarito', '') or row.get('resposta', ''),
                    
                    # AQUI ESTÁ A CORREÇÃO: Mapeando as alternativas
                    texto_01=achar_texto(['01', 'prop_01', 'texto_01', 'p1']),
                    texto_02=achar_texto(['02', 'prop_02', 'texto_02', 'p2']),
                    texto_04=achar_texto(['04', 'prop_04', 'texto_04', 'p4']),
                    texto_08=achar_texto(['08', 'prop_08', 'texto_08', 'p8']),
                    texto_16=achar_texto(['16', 'prop_16', 'texto_16', 'p16']),
                    texto_32=achar_texto(['32', 'prop_32', 'texto_32', 'p32']),
                    texto_64=achar_texto(['64', 'prop_64', 'texto_64', 'p64']),
                )
                count += 1
            except Exception as e:
                print(f"Erro na linha {count+1}: {e}")

        file.close()
        self.stdout.write(self.style.SUCCESS(f'SUCESSO! {count} questões importadas.'))