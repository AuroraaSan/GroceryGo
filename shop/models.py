from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
import os


# Create your models here.
class Category(models.Model):
    cat_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    parent_cat = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.category_name
    
    class Meta:
        ordering = ['category_name']
        indexes = [
        models.Index(fields=['category_name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.category_name])

class Company(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    contact_num = models.CharField(max_length=15, null=True)
    email = models.EmailField(blank=True, null=True)
    NATIONALITY_CHOICES = [
    ('AFG', 'Afghanistan'),
    ('ALB', 'Albania'),
    ('DZA', 'Algeria'),
    ('ASM', 'American Samoa'),
    ('AND', 'Andorra'),
    ('AGO', 'Angola'),
    ('AIA', 'Anguilla'),
    ('ATA', 'Antarctica'),
    ('ATG', 'Antigua and Barbuda'),
    ('ARG', 'Argentina'),
    ('ARM', 'Armenia'),
    ('ABW', 'Aruba'),
    ('AUS', 'Australia'),
    ('AUT', 'Austria'),
    ('AZE', 'Azerbaijan'),
    ('BHS', 'Bahamas (the)'),
    ('BHR', 'Bahrain'),
    ('BGD', 'Bangladesh'),
    ('BRB', 'Barbados'),
    ('BLR', 'Belarus'),
    ('BEL', 'Belgium'),
    ('BLZ', 'Belize'),
    ('BEN', 'Benin'),
    ('BMU', 'Bermuda'),
    ('BTN', 'Bhutan'),
    ('BOL', 'Bolivia (Plurinational State of)'),
    ('BES', 'Bonaire, Sint Eustatius and Saba'),
    ('BIH', 'Bosnia and Herzegovina'),
    ('BWA', 'Botswana'),
    ('BVT', 'Bouvet Island'),
    ('BRA', 'Brazil'),
    ('IOT', 'British Indian Ocean Territory (the)'),
    ('BRN', 'Brunei Darussalam'),
    ('BGR', 'Bulgaria'),
    ('BFA', 'Burkina Faso'),
    ('BDI', 'Burundi'),
    ('CPV', 'Cabo Verde'),
    ('KHM', 'Cambodia'),
    ('CMR', 'Cameroon'),
    ('CAN', 'Canada'),
    ('CYM', 'Cayman Islands (the)'),
    ('CAF', 'Central African Republic (the)'),
    ('TCD', 'Chad'),
    ('CHL', 'Chile'),
    ('CHN', 'China'),
    ('CXR', 'Christmas Island'),
    ('CCK', 'Cocos (Keeling) Islands (the)'),
    ('COL', 'Colombia'),
    ('COM', 'Comoros (the)'),
    ('COD', 'Congo (the Democratic Republic of the)'),
    ('COG', 'Congo (the)'),
    ('COK', 'Cook Islands (the)'),
    ('CRI', 'Costa Rica'),
    ('HRV', 'Croatia'),
    ('CUB', 'Cuba'),
    ('CUW', 'Curaçao'),
    ('CYP', 'Cyprus'),
    ('CZE', 'Czechia'),
    ('CIV', "Côte d'Ivoire"),
    ('DNK', 'Denmark'),
    ('DJI', 'Djibouti'),
    ('DMA', 'Dominica'),
    ('DOM', 'Dominican Republic (the)'),
    ('ECU', 'Ecuador'),
    ('EGY', 'Egypt'),
    ('SLV', 'El Salvador'),
    ('GNQ', 'Equatorial Guinea'),
    ('ERI', 'Eritrea'),
    ('EST', 'Estonia'),
    ('SWZ', 'Eswatini'),
    ('ETH', 'Ethiopia'),
    ('FLK', 'Falkland Islands (the) [Malvinas]'),
    ('FRO', 'Faroe Islands (the)'),
    ('FJI', 'Fiji'),
    ('FIN', 'Finland'),
    ('FRA', 'France'),
    ('GUF', 'French Guiana'),
    ('PYF', 'French Polynesia'),
    ('ATF', 'French Southern Territories (the)'),
    ('GAB', 'Gabon'),
    ('GMB', 'Gambia (the)'),
    ('GEO', 'Georgia'),
    ('DEU', 'Germany'),
    ('GHA', 'Ghana'),
    ('GIB', 'Gibraltar'),
    ('GRC', 'Greece'),
    ('GRL', 'Greenland'),
    ('GRD', 'Grenada'),
    ('GLP', 'Guadeloupe'),
    ('GUM', 'Guam'),
    ('GTM', 'Guatemala'),
    ('GGY', 'Guernsey'),
    ('GIN', 'Guinea'),
    ('GNB', 'Guinea-Bissau'),
    ('GUY', 'Guyana'),
    ('HTI', 'Haiti'),
    ('HMD', 'Heard Island and McDonald Islands'),
    ('VAT', 'Holy See (the)'),
    ('HND', 'Honduras'),
    ('HKG', 'Hong Kong'),
    ('HUN', 'Hungary'),
    ('ISL', 'Iceland'),
    ('IND', 'India'),
    ('IDN', 'Indonesia'),
    ('IRN', 'Iran (Islamic Republic of)'),
    ('IRQ', 'Iraq'),
    ('IRL', 'Ireland'),
    ('IMN', 'Isle of Man'),
    ('ISR', 'Israel'),
    ('ITA', 'Italy'),
    ('JAM', 'Jamaica'),
    ('JPN', 'Japan'),
    ('JEY', 'Jersey'),
    ('JOR', 'Jordan'),
    ('KAZ', 'Kazakhstan'),
    ('KEN', 'Kenya'),
    ('KIR', 'Kiribati'),
    ('PRK', "Korea (the Democratic People's Republic of)"),
    ('KOR', 'Korea (the Republic of)'),
    ('KWT', 'Kuwait'),
    ('KGZ', 'Kyrgyzstan'),
    ('LAO', "Lao People's Democratic Republic (the)"),
    ('LVA', 'Latvia'),
    ('LBN', 'Lebanon'),
    ('LSO', 'Lesotho'),
    ('LBR', 'Liberia'),
    ('LBY', 'Libya'),
    ('LIE', 'Liechtenstein'),
    ('LTU', 'Lithuania'),
    ('LUX', 'Luxembourg'),
    ('MAC', 'Macao'),
    ('MDG', 'Madagascar'),
    ('MWI', 'Malawi'),
    ('MYS', 'Malaysia'),
    ('MDV', 'Maldives'),
    ('MLI', 'Mali'),
    ('MLT', 'Malta'),
    ('MHL', 'Marshall Islands (the)'),
    ('MTQ', 'Martinique'),
    ('MRT', 'Mauritania'),
    ('MUS', 'Mauritius'),
    ('MYT', 'Mayotte'),
    ('MEX', 'Mexico'),
    ('FSM', 'Micronesia (Federated States of)'),
    ('MDA', 'Moldova (the Republic of)'),
    ('MCO', 'Monaco'),
    ('MNG', 'Mongolia'),
    ('MNE', 'Montenegro'),
    ('MSR', 'Montserrat'),
    ('MAR', 'Morocco'),
    ('MOZ', 'Mozambique'),
    ('MMR', 'Myanmar'),
    ('NAM', 'Namibia'),
    ('NRU', 'Nauru'),
    ('NPL', 'Nepal'),
    ('NLD', 'Netherlands (the)'),
    ('NCL', 'New Caledonia'),
    ('NZL', 'New Zealand'),
    ('NIC', 'Nicaragua'),
    ('NER', 'Niger (the)'),
    ('NGA', 'Nigeria'),
    ('NIU', 'Niue'),
    ('NFK', 'Norfolk Island'),
    ('MNP', 'Northern Mariana Islands (the)'),
    ('NOR', 'Norway'),
    ('OMN', 'Oman'),
    ('PAK', 'Pakistan'),
    ('PLW', 'Palau'),
    ('PSE', 'Palestine, State of'),
    ('PAN', 'Panama'),
    ('PNG', 'Papua New Guinea'),
    ('PRY', 'Paraguay'),
    ('PER', 'Peru'),
    ('PHL', 'Philippines (the)'),
    ('PCN', 'Pitcairn'),
    ('POL', 'Poland'),
    ('PRT', 'Portugal'),
    ('PRI', 'Puerto Rico'),
    ('QAT', 'Qatar'),
    ('MKD', 'Republic of North Macedonia'),
    ('ROU', 'Romania'),
    ('RUS', 'Russian Federation (the)'),
    ('RWA', 'Rwanda'),
    ('REU', 'Réunion'),
    ('BLM', 'Saint Barthélemy'),
    ('SHN', 'Saint Helena, Ascension and Tristan da Cunha'),
    ('KNA', 'Saint Kitts and Nevis'),
    ('LCA', 'Saint Lucia'),
    ('MAF', 'Saint Martin (French part)'),
    ('SPM', 'Saint Pierre and Miquelon'),
    ('VCT', 'Saint Vincent and the Grenadines'),
    ('WSM', 'Samoa'),
    ('SMR', 'San Marino'),
    ('STP', 'Sao Tome and Principe'),
    ('SAU', 'Saudi Arabia'),
    ('SEN', 'Senegal'),
    ('SRB', 'Serbia'),
    ('SYC', 'Seychelles'),
    ('SLE', 'Sierra Leone'),
    ('SGP', 'Singapore'),
    ('SXM', 'Sint Maarten (Dutch part)'),
    ('SVK', 'Slovakia'),
    ('SVN', 'Slovenia'),
    ('SLB', 'Solomon Islands'),
    ('SOM', 'Somalia'),
    ('ZAF', 'South Africa'),
    ('SGS', 'South Georgia and the South Sandwich Islands'),
    ('SSD', 'South Sudan'),
    ('ESP', 'Spain'),
    ('LKA', 'Sri Lanka'),
    ('SDN', 'Sudan (the)'),
    ('SUR', 'Suriname'),
    ('SJM', 'Svalbard and Jan Mayen'),
    ('SWE', 'Sweden'),
    ('CHE', 'Switzerland'),
    ('SYR', 'Syrian Arab Republic'),
    ('TWN', 'Taiwan (Province of China)'),
    ('TJK', 'Tajikistan'),
    ('TZA', 'Tanzania, United Republic of'),
    ('THA', 'Thailand'),
    ('TLS', 'Timor-Leste'),
    ('TGO', 'Togo'),
    ('TKL', 'Tokelau'),
    ('TON', 'Tonga'),
    ('TTO', 'Trinidad and Tobago'),
    ('TUN', 'Tunisia'),
    ('TUR', 'Turkey'),
    ('TKM', 'Turkmenistan'),
    ('TCA', 'Turks and Caicos Islands (the)'),
    ('TUV', 'Tuvalu'),
    ('UGA', 'Uganda'),
    ('UKR', 'Ukraine'),
    ('ARE', 'United Arab Emirates (the)'),
    ('GBR', 'United Kingdom of Great Britain and Northern Ireland (the)'),
    ('UMI', 'United States Minor Outlying Islands (the)'),
    ('USA', 'United States of America (the)'),
    ('URY', 'Uruguay'),
    ('UZB', 'Uzbekistan'),
    ('VUT', 'Vanuatu'),
    ('VEN', 'Venezuela (Bolivarian Republic of)'),
    ('VNM', 'Viet Nam'),
    ('VGB', 'Virgin Islands (British)'),
    ('VIR', 'Virgin Islands (U.S.)'),
    ('WLF', 'Wallis and Futuna'),
    ('ESH', 'Western Sahara'),
    ('YEM', 'Yemen'),
    ('ZMB', 'Zambia'),
    ('ZWE', 'Zimbabwe'),
    ('ALA', 'Åland Islands'),
]
    nationality = models.CharField(max_length=3, choices=NATIONALITY_CHOICES)
    speciality = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['company_name']
        indexes = [
        models.Index(fields=['company_name']),
        ]
        verbose_name = 'company'
        verbose_name_plural = 'companies'
    
    

    
class Product(models.Model):
    p_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    discount = models.FloatField(default=0.0, validators=[
        MaxValueValidator(100.0),
        MinValueValidator(0.0)
    ])
    manfacture_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=False, blank=False)
    purchased_gen = models.IntegerField(default=0)
    purchased_24 = models.IntegerField(default=0)
    p_image = models.ImageField(upload_to='products/', blank=True)
    company= models.ForeignKey(Company, on_delete=models.SET_DEFAULT, null=True, default=1)
    cat = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['product_name']
        indexes = [
            models.Index(fields=['p_id', 'slug']),
            models.Index(fields=['product_name']),
        ]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.p_id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)

        if self.p_image and not hasattr(self.p_image, 'original_name'):
            try:
                file_name, ext = os.path.splitext(self.p_image.name)
                new_name = f"{slugify(self.product_name)}{ext}"
                self.p_image.name = new_name
                setattr(self.p_image, 'original_name', file_name)
            except Exception as e:
                # If there's an error, revert to the original file name
                self.p_image.name = file_name
                setattr(self.p_image, 'original_name', file_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name
