
import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from questoes.models import Questao

class Command(BaseCommand):
    help = "Importa questões do CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            '--arquivo',
            default='questoes_prova.csv',
            help='Caminho para o arquivo CSV (padrão: questoes_prova.csv)'
        )
        parser.add_argument(
            '--atualizar',
            action='store_true',
            help='Atualiza registros existentes (match pelo campo numero)'
        )

    def handle(self, *args, **options):
        caminho = options['arquivo']
        atualizar = options['atualizar']

        try:
            with open(caminho, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # Valide as colunas esperadas
                colunas_obrigatorias = ['NumeroQuestao', 'Enunciado']
                for col in colunas_obrigatorias:
                    if col not in reader.fieldnames:
                        raise CommandError(
                            f"Coluna obrigatória ausente no CSV: '{col}'. "
                            f"Encontradas: {reader.fieldnames}"
                        )

                criados = 0
                atualizados = 0
                pulados = 0

                with transaction.atomic():
                    for i, row in enumerate(reader, start=1):
                        try:
                            numero = int(row['NumeroQuestao'])
                        except (ValueError, TypeError):
                            self.stderr.write(f"[linha {i}] NumeroQuestao inválido: {row.get('NumeroQuestao')}. Pulando.")
                            pulados += 1
                            continue

                        dados = {
                            'enunciado': row.get('Enunciado', '').strip(),
                            'alternativa_01': (row.get('Alternativa_01') or '').strip(),
                            'alternativa_02': (row.get('Alternativa_02') or '').strip(),
                            'alternativa_04': (row.get('Alternativa_04') or '').strip(),
                            'alternativa_08': (row.get('Alternativa_08') or '').strip(),
                            'alternativa_16': (row.get('Alternativa_16') or '').strip(),
                            'alternativa_32': (row.get('Alternativa_32') or '').strip(),
                            'alternativa_64': (row.get('Alternativa_64') or '').strip(),
                            'resposta': (row.get('Resposta') or '').strip(),
                        }

                        if atualizar:
                            obj, created = Questao.objects.update_or_create(
                                numero=numero,
                                defaults=dados
                            )
                            if created:
                                criados += 1
                            else:
                                atualizados += 1
                        else:
                            # Evita duplicado simples quando não atualiza
                            if Questao.objects.filter(numero=numero).exists():
                                self.stderr.write(f"[linha {i}] Questão {numero} já existe. Use --atualizar para sobrescrever.")
                                pulados += 1
                                continue
                            Questao.objects.create(numero=numero, **dados)
                            criados += 1

                self.stdout.write(self.style.SUCCESS(
                    f"Importação concluída. Criados: {criados}, Atualizados: {atualizados}, Pulados: {pulados}"
                ))

        except FileNotFoundError:
            raise CommandError(f"Arquivo não encontrado: {caminho}")
        except csv.Error as e:
            raise CommandError(f"Erro ao ler o CSV: {e}")