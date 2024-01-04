import sys
import os
import re
from decimal import Decimal
from prettytable import PrettyTable

def read_out_file(file_path, file_type):
    f = open(file_path, 'r')
    n_linha = 0
    data = {}
    
    for key in nome_colunas:
        data[nome_colunas[key]] = []
    
    line = f.readline()
    while line:
        n_linha += 1
        
        if n_linha > 1 or file_type == 'traj':
            line = line.strip()
            values = re.split(r'\s+', line)
            
            n_coluna = 0
            for value in values:
                value = value.strip()
                
                value_dict = { 'valor': value, 'linha': n_linha }
                data[nome_colunas[n_coluna]].append(value_dict)
                    
                n_coluna += 1
    
        line = f.readline()

    f.close()
    return data

def strip_left_zeros(s):
    if len(s) > 0:
        if s[0] == '-':
            s = s[0] + s[1:].lstrip('0')
        else:
            s = s.lstrip('0')
            
    return s
        
def compare_values(out_value, ref_value):
    num_dig_min = 12
    
    out_split = out_value.split('e')
    ref_split = ref_value.split('e')
    
    out_mant = out_split[0]
    out_exp = None
    if len(out_split) > 1:
        out_exp = strip_left_zeros(out_split[1])
    
    ref_mant = ref_split[0]
    ref_exp = None
    if len(ref_split) > 1:
        ref_exp = strip_left_zeros(ref_split[1])

    
    out_mant_split = out_mant.split('.')
    ref_mant_split = ref_mant.split('.')
    
    out_int = strip_left_zeros(out_mant_split[0])
    
    out_dec = None
    if len(out_mant_split) > 1:
        out_dec = out_mant_split[1]
        
    ref_int = strip_left_zeros(ref_mant_split[0])
    
    ref_dec = None
    if len(ref_mant_split) > 1:
        ref_dec = ref_mant_split[1]
        
    
    if out_int == ref_int and out_exp == ref_exp:
        if out_dec == ref_dec:
            return True
        
        elif out_dec is not None and ref_dec is not None:
            num_dig_out_int = sum(char.isdigit() for char in out_int)
            dig_parte_decimal = num_dig_min - num_dig_out_int
            
            out_dec = Decimal('0.' + out_dec)
            ref_dec = Decimal('0.' + ref_dec)
            
            diff = format(abs(out_dec - ref_dec), 'f')
            diff_dec = diff.split('.')[1]
            
            if diff_dec is not None:
                i = 0
                while i<len(diff_dec) and diff_dec[i] == '0':
                    i += 1
                     
                if i >= dig_parte_decimal:
                    return True
                else:
                    return False
                
            else:
                return False
                        
        else:
            return False
    
    else:
        return False
    
def compare_outputs(output_data, comparison_data, file_type):
        no_errors = True
        primeira_coluna = next(iter(output_data))
        
        if len(output_data[primeira_coluna]) == len(comparison_data[primeira_coluna]):
            tabela_erros = PrettyTable(['Linha', 'Coluna', 'Valor de referência', 'Valor calculado']) 
            tabela_erros.title = f'Erros encontrados • {file_type.upper()}'
            
            for coluna in output_data:
                for i in range(len(output_data[coluna])):
                    out_value = output_data[coluna][i]
                    ref_value = comparison_data[coluna][i]
                                    
                    equal = compare_values(out_value['valor'], ref_value['valor'])
                    
                    if not equal:
                        tabela_erros.add_row([out_value['linha'], coluna, ref_value['valor'], out_value['valor']])
                        no_errors = False
                        
            if no_errors:
                print('Não foram encontrados erros.')
            else:
                print(tabela_erros)
                                    
        else:
            print('O output calculado e o output de referência têm nº de linhas diferente.')
                
                
if len(sys.argv) >= 2:
    file_type = sys.argv[1]
    reference_outputs_folder_path = './sequential/'
    
    if file_type == 'average':
        nome_colunas = {0: 'Total Time (s)', 1: 'T (K)', 2: 'P (Pa)', 3: 'PV/nT (J/(mol K))', 4: 'Z', 5: 'V (m^3)', 6: 'N'}
        output_file_path =  'cp_average.txt'
        comparison_file_path = reference_outputs_folder_path + 'cp_average.txt'
        
    elif file_type == 'output':
        nome_colunas = {0: 'time (s)', 1: 'T(t) (K)', 2: 'P(t) (Pa)', 3: 'Kinetic En. (n.u.)', 4: 'Potential En. (n.u.)', 5: 'Total En. (n.u.)'}
        output_file_path = 'cp_output.txt'
        comparison_file_path =  reference_outputs_folder_path + 'cp_output.txt'
        
    elif file_type == 'traj':
        nome_colunas = {0: '-'}
        output_file_path =  'cp_traj.xyz'
        comparison_file_path = reference_outputs_folder_path + 'cp_traj.xyz'
        
    else:
        print(f"Opção '{file_type}' inválida.")
        exit(0)
        
    if len(sys.argv) >= 3:
        output_file_path = sys.argv[2]
        
        if len(sys.argv) >= 4:
            comparison_file_path = sys.argv[3]

    output_data = read_out_file(output_file_path, file_type)
    comparison_data = read_out_file(comparison_file_path, file_type)
    
    compare_outputs(output_data, comparison_data, file_type)
    
else:
    print("Não foi introduzida uma opção. Introduza 'average', 'output' ou 'traj' conforme o ficheiro que pretenda verificar.")
