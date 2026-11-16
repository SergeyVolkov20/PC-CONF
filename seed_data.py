import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'someproject.settings')
django.setup()

from someapp.models import Category, Product, Specification

def seed():
    print("Очистка старых данных...")
    Specification.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()

    print("Создание категорий...")
    cpu_cat = Category.objects.create(name='Процессоры', slug='cpu', sort_order=1)
    mb_cat = Category.objects.create(name='Материнские платы', slug='motherboard', sort_order=2)
    ram_cat = Category.objects.create(name='Оперативная память', slug='ram', sort_order=3)
    gpu_cat = Category.objects.create(name='Видеокарты', slug='gpu', sort_order=4)
    psu_cat = Category.objects.create(name='Блоки питания', slug='psu', sort_order=5)
    case_cat = Category.objects.create(name='Корпуса', slug='case', sort_order=6)
    storage_cat = Category.objects.create(name='Накопители', slug='storage', sort_order=7)
    cooling_cat = Category.objects.create(name='Охлаждение', slug='cooling', sort_order=8)

    print("Создание товаров...")

    cpu1 = Product.objects.create(category=cpu_cat, name='Intel Core i5-13600KF', brand='Intel', price=25000, stock=10)
    Specification.objects.create(product=cpu1, spec_key='socket', spec_value='LGA1700')
    Specification.objects.create(product=cpu1, spec_key='tdp', spec_value='125')

    cpu2 = Product.objects.create(category=cpu_cat, name='Intel Core i7-13700K', brand='Intel', price=38000, stock=5)
    Specification.objects.create(product=cpu2, spec_key='socket', spec_value='LGA1700')
    Specification.objects.create(product=cpu2, spec_key='tdp', spec_value='125')

    cpu3 = Product.objects.create(category=cpu_cat, name='AMD Ryzen 5 7600X', brand='AMD', price=22000, stock=8)
    Specification.objects.create(product=cpu3, spec_key='socket', spec_value='AM5')
    Specification.objects.create(product=cpu3, spec_key='tdp', spec_value='105')

    cpu4 = Product.objects.create(category=cpu_cat, name='AMD Ryzen 7 7700X', brand='AMD', price=32000, stock=4)
    Specification.objects.create(product=cpu4, spec_key='socket', spec_value='AM5')
    Specification.objects.create(product=cpu4, spec_key='tdp', spec_value='105')

    mb1 = Product.objects.create(category=mb_cat, name='ASUS PRIME Z790-A', brand='ASUS', price=30000, stock=5)
    Specification.objects.create(product=mb1, spec_key='socket', spec_value='LGA1700')
    Specification.objects.create(product=mb1, spec_key='memory_type', spec_value='DDR5')
    Specification.objects.create(product=mb1, spec_key='form_factor', spec_value='ATX')

    mb2 = Product.objects.create(category=mb_cat, name='MSI PRO Z790-P', brand='MSI', price=22000, stock=7)
    Specification.objects.create(product=mb2, spec_key='socket', spec_value='LGA1700')
    Specification.objects.create(product=mb2, spec_key='memory_type', spec_value='DDR5')
    Specification.objects.create(product=mb2, spec_key='form_factor', spec_value='ATX')

    mb3 = Product.objects.create(category=mb_cat, name='MSI MAG B650 Tomahawk', brand='MSI', price=18000, stock=6)
    Specification.objects.create(product=mb3, spec_key='socket', spec_value='AM5')
    Specification.objects.create(product=mb3, spec_key='memory_type', spec_value='DDR5')
    Specification.objects.create(product=mb3, spec_key='form_factor', spec_value='ATX')

    mb4 = Product.objects.create(category=mb_cat, name='Gigabyte B650M DS3H', brand='Gigabyte', price=14000, stock=10)
    Specification.objects.create(product=mb4, spec_key='socket', spec_value='AM5')
    Specification.objects.create(product=mb4, spec_key='memory_type', spec_value='DDR5')
    Specification.objects.create(product=mb4, spec_key='form_factor', spec_value='Micro-ATX')

    ram1 = Product.objects.create(category=ram_cat, name='Kingston Fury DDR5 16GB', brand='Kingston', price=8000, stock=20)
    Specification.objects.create(product=ram1, spec_key='memory_type', spec_value='DDR5')
    Specification.objects.create(product=ram1, spec_key='tdp', spec_value='5')

    ram2 = Product.objects.create(category=ram_cat, name='G.Skill Trident Z5 32GB', brand='G.Skill', price=15000, stock=15)
    Specification.objects.create(product=ram2, spec_key='memory_type', spec_value='DDR5')
    Specification.objects.create(product=ram2, spec_key='tdp', spec_value='10')

    ram3 = Product.objects.create(category=ram_cat, name='Corsair Vengeance 16GB', brand='Corsair', price=7500, stock=12)
    Specification.objects.create(product=ram3, spec_key='memory_type', spec_value='DDR5')
    Specification.objects.create(product=ram3, spec_key='tdp', spec_value='5')

    gpu1 = Product.objects.create(category=gpu_cat, name='NVIDIA RTX 4070', brand='Palit', price=60000, stock=3)
    Specification.objects.create(product=gpu1, spec_key='tdp', spec_value='200')
    Specification.objects.create(product=gpu1, spec_key='length', spec_value='280')

    gpu2 = Product.objects.create(category=gpu_cat, name='NVIDIA RTX 4060 Ti', brand='MSI', price=45000, stock=5)
    Specification.objects.create(product=gpu2, spec_key='tdp', spec_value='160')
    Specification.objects.create(product=gpu2, spec_key='length', spec_value='240')

    gpu3 = Product.objects.create(category=gpu_cat, name='AMD RX 7800 XT', brand='Sapphire', price=55000, stock=4)
    Specification.objects.create(product=gpu3, spec_key='tdp', spec_value='263')
    Specification.objects.create(product=gpu3, spec_key='length', spec_value='320')

    psu1 = Product.objects.create(category=psu_cat, name='БП 650W', brand='DeepCool', price=6000, stock=15)
    Specification.objects.create(product=psu1, spec_key='power', spec_value='650')

    psu2 = Product.objects.create(category=psu_cat, name='БП 750W', brand='Cougar', price=8500, stock=10)
    Specification.objects.create(product=psu2, spec_key='power', spec_value='750')

    psu3 = Product.objects.create(category=psu_cat, name='БП 1000W', brand='Corsair', price=15000, stock=5)
    Specification.objects.create(product=psu3, spec_key='power', spec_value='1000')

    case1 = Product.objects.create(category=case_cat, name='Zalman i3 Neo', brand='Zalman', price=4000, stock=10)
    Specification.objects.create(product=case1, spec_key='form_factor_support', spec_value='ATX, Micro-ATX')
    Specification.objects.create(product=case1, spec_key='max_gpu_length', spec_value='330')

    case2 = Product.objects.create(category=case_cat, name='Lian Li Lancool 216', brand='Lian Li', price=9000, stock=6)
    Specification.objects.create(product=case2, spec_key='form_factor_support', spec_value='ATX, Micro-ATX')
    Specification.objects.create(product=case2, spec_key='max_gpu_length', spec_value='392')

    case3 = Product.objects.create(category=case_cat, name='DeepCool CH510', brand='DeepCool', price=5500, stock=8)
    Specification.objects.create(product=case3, spec_key='form_factor_support', spec_value='ATX, Micro-ATX')
    Specification.objects.create(product=case3, spec_key='max_gpu_length', spec_value='380')

    storage1 = Product.objects.create(category=storage_cat, name='SSD Samsung 980 1TB', brand='Samsung', price=9000, stock=10)
    Specification.objects.create(product=storage1, spec_key='type', spec_value='SSD')

    storage2 = Product.objects.create(category=storage_cat, name='SSD Kingston NV2 500GB', brand='Kingston', price=4500, stock=20)
    Specification.objects.create(product=storage2, spec_key='type', spec_value='SSD')

    cooler1 = Product.objects.create(category=cooling_cat, name='DeepCool AK620', brand='DeepCool', price=5000, stock=5)
    Specification.objects.create(product=cooler1, spec_key='tdp', spec_value='10')

    cooler2 = Product.objects.create(category=cooling_cat, name='ID-Cooling SE-224-XT', brand='ID-Cooling', price=2500, stock=10)
    Specification.objects.create(product=cooler2, spec_key='tdp', spec_value='5')

    print("✅ Тестовые данные успешно добавлены!")

if __name__ == '__main__':
    seed()