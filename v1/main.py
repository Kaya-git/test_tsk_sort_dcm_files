import pydicom
import os
import shutil


def create_folder(folder_path: str, folder_name: str) -> None:
    """
    Функция для создания папки
    """
    if not os.path.exists(f'{folder_path}\\{folder_name}'):
        os.mkdir(f'{folder_path}\\{folder_name}')

def write_down_relations(dcm: str, original_path: str, final_path: str) -> None:
    """
    Создаем файл и записываем сопоставленные пути
    """
    text = f'Название файла: "{dcm}", изначальный путь к файлу: {original_path}, конечный путь файла: {final_path}'
    relations = open('relations.txt', 'a')
    relations.write(text)
    relations.write('\n')
    relations.close

def create_new_structure(dc: str, dcm: str, new_path: str) -> str:
    """
    Создаем новую структуру
    """
    create_folder(new_path, dc.StudyInstanceUID)
    first_layer = f'{new_path}\\{dc.StudyInstanceUID}'
    create_folder(first_layer, dc.SeriesInstanceUID)
    second_layer = f'{first_layer}\\{dc.SeriesInstanceUID}'
    shutil.copy2(f'{dir_name}\\{dcm}', f'{second_layer}\\{dc.SOPInstanceUID}.dcm')
    final_path = os.path.abspath(f'{second_layer}\\{dc.SOPInstanceUID}.dcm')
    return final_path

def sort_and_anonymize(DIR_NAME: str, new_path: str) -> None:
    """
    Анонимизируем имена пациентов и сортируем по папкам
    """
    dir_name = os.listdir(DIR_NAME)
    for dcm in dir_name:
        original_path = os.path.abspath(f'src\\{dcm}')
        dc = pydicom.dcmread(original_path)
        dc.PatientName = ''
        final_path = create_new_structure(dc, dcm, new_path)
        write_down_relations(dcm, original_path, final_path)

if __name__ == '__main__':
    new_path = 'C:\\Dev\\test_tsk_sort_dcm_files\\v1\\new_structure'
    dir_name = 'C:\\Dev\\test_tsk_sort_dcm_files\\v1\\src'
    sort_and_anonymize(dir_name, new_path)
    