from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Телефон должен быть заполнен в формате: '+999999999'. Максимум 15 цифр.")
