from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.db.models import signals
from django.dispatch import receiver
from django.db.models import F, Sum
from django.db.models.signals import post_save, post_delete


# Create your models here.
class Category(models.Model):
    cat_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    parent_cat = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    product_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ["category_name"]
        indexes = [
            models.Index(fields=["category_name"]),
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.category_name])


class Company(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    contact_num = models.CharField(max_length=15, null=True)
    email = models.EmailField(blank=True, null=True)
    NATIONALITY_CHOICES = [
        ("AFG", "Afghanistan"),
        ("ALB", "Albania"),
        ("DZA", "Algeria"),
        ("AND", "Andorra"),
        ("AGO", "Angola"),
        ("ATG", "Antigua and Barbuda"),
        ("ARG", "Argentina"),
        ("ARM", "Armenia"),
        ("AUS", "Australia"),
        ("AUT", "Austria"),
        ("AZE", "Azerbaijan"),
        ("BHS", "Bahamas"),
        ("BHR", "Bahrain"),
        ("BGD", "Bangladesh"),
        ("BRB", "Barbados"),
        ("BLR", "Belarus"),
        ("BEL", "Belgium"),
        ("BLZ", "Belize"),
        ("BEN", "Benin"),
        ("BTN", "Bhutan"),
        ("BOL", "Bolivia"),
        ("BIH", "Bosnia and Herzegovina"),
        ("BWA", "Botswana"),
        ("BRA", "Brazil"),
        ("BRN", "Brunei"),
        ("BGR", "Bulgaria"),
        ("BFA", "Burkina Faso"),
        ("BDI", "Burundi"),
        ("CPV", "Cabo Verde"),
        ("KHM", "Cambodia"),
        ("CMR", "Cameroon"),
        ("CAN", "Canada"),
        ("CAF", "Central African Republic"),
        ("TCD", "Chad"),
        ("CHL", "Chile"),
        ("CHN", "China"),
        ("COL", "Colombia"),
        ("COM", "Comoros"),
        ("COG", "Congo"),
        ("CRI", "Costa Rica"),
        ("HRV", "Croatia"),
        ("CUB", "Cuba"),
        ("CYP", "Cyprus"),
        ("CZE", "Czechia"),
        ("DNK", "Denmark"),
        ("DJI", "Djibouti"),
        ("DMA", "Dominica"),
        ("DOM", "Dominican Republic"),
        ("ECU", "Ecuador"),
        ("EGY", "Egypt"),
        ("SLV", "El Salvador"),
        ("GNQ", "Equatorial Guinea"),
        ("ERI", "Eritrea"),
        ("EST", "Estonia"),
        ("SWZ", "Eswatini"),
        ("ETH", "Ethiopia"),
        ("FJI", "Fiji"),
        ("FIN", "Finland"),
        ("FRA", "France"),
        ("GAB", "Gabon"),
        ("GMB", "Gambia"),
        ("GEO", "Georgia"),
        ("DEU", "Germany"),
        ("GHA", "Ghana"),
        ("GRC", "Greece"),
        ("GRD", "Grenada"),
        ("GTM", "Guatemala"),
        ("GIN", "Guinea"),
        ("GNB", "Guinea-Bissau"),
        ("GUY", "Guyana"),
        ("HTI", "Haiti"),
        ("HND", "Honduras"),
        ("HUN", "Hungary"),
        ("ISL", "Iceland"),
        ("IND", "India"),
        ("IDN", "Indonesia"),
        ("IRN", "Iran"),
        ("IRQ", "Iraq"),
        ("IRL", "Ireland"),
        ("ISR", "Israel"),
        ("ITA", "Italy"),
        ("JAM", "Jamaica"),
        ("JPN", "Japan"),
        ("JOR", "Jordan"),
        ("KAZ", "Kazakhstan"),
        ("KEN", "Kenya"),
        ("KIR", "Kiribati"),
        ("PRK", "Korea (North)"),
        ("KOR", "Korea (South)"),
        ("XKX", "Kosovo"),
        ("KWT", "Kuwait"),
        ("KGZ", "Kyrgyzstan"),
        ("LAO", "Laos"),
        ("LVA", "Latvia"),
        ("LBN", "Lebanon"),
        ("LSO", "Lesotho"),
        ("LBR", "Liberia"),
        ("LBY", "Libya"),
        ("LIE", "Liechtenstein"),
        ("LTU", "Lithuania"),
        ("LUX", "Luxembourg"),
        ("MDG", "Madagascar"),
        ("MWI", "Malawi"),
        ("MYS", "Malaysia"),
        ("MDV", "Maldives"),
        ("MLI", "Mali"),
        ("MLT", "Malta"),
        ("MHL", "Marshall Islands"),
        ("MRT", "Mauritania"),
        ("MUS", "Mauritius"),
        ("MEX", "Mexico"),
        ("FSM", "Micronesia"),
        ("MDA", "Moldova"),
        ("MCO", "Monaco"),
        ("MNG", "Mongolia"),
        ("MNE", "Montenegro"),
        ("MAR", "Morocco"),
        ("MOZ", "Mozambique"),
        ("MMR", "Myanmar"),
        ("NAM", "Namibia"),
        ("NRU", "Nauru"),
        ("NPL", "Nepal"),
        ("NLD", "Netherlands"),
        ("NZL", "New Zealand"),
        ("NIC", "Nicaragua"),
        ("NER", "Niger"),
        ("NGA", "Nigeria"),
        ("MKD", "North Macedonia"),
        ("NOR", "Norway"),
        ("OMN", "Oman"),
        ("PAK", "Pakistan"),
        ("PLW", "Palau"),
        ("PAN", "Panama"),
        ("PNG", "Papua New Guinea"),
        ("PRY", "Paraguay"),
        ("PER", "Peru"),
        ("PHL", "Philippines"),
        ("POL", "Poland"),
        ("PRT", "Portugal"),
        ("QAT", "Qatar"),
        ("ROU", "Romania"),
        ("RUS", "Russia"),
        ("RWA", "Rwanda"),
        ("KNA", "Saint Kitts and Nevis"),
        ("LCA", "Saint Lucia"),
        ("VCT", "Saint Vincent and the Grenadines"),
        ("WSM", "Samoa"),
        ("SMR", "San Marino"),
        ("STP", "Sao Tome and Principe"),
        ("SAU", "Saudi Arabia"),
        ("SEN", "Senegal"),
        ("SRB", "Serbia"),
        ("SYC", "Seychelles"),
        ("SLE", "Sierra Leone"),
        ("SGP", "Singapore"),
        ("SVK", "Slovakia"),
        ("SVN", "Slovenia"),
        ("SLB", "Solomon Islands"),
        ("SOM", "Somalia"),
        ("ZAF", "South Africa"),
        ("SSD", "South Sudan"),
        ("ESP", "Spain"),
        ("LKA", "Sri Lanka"),
        ("SDN", "Sudan"),
        ("SUR", "Suriname"),
        ("SWE", "Sweden"),
        ("CHE", "Switzerland"),
        ("SYR", "Syria"),
        ("TWN", "Taiwan"),
        ("TJK", "Tajikistan"),
        ("TZA", "Tanzania"),
        ("THA", "Thailand"),
        ("TLS", "Timor-Leste"),
        ("TGO", "Togo"),
        ("TON", "Tonga"),
        ("TTO", "Trinidad and Tobago"),
        ("TUN", "Tunisia"),
        ("TUR", "Turkey"),
        ("TKM", "Turkmenistan"),
        ("TUV", "Tuvalu"),
        ("UGA", "Uganda"),
        ("UKR", "Ukraine"),
        ("ARE", "United Arab Emirates"),
        ("GBR", "United Kingdom"),
        ("USA", "United States"),
        ("URY", "Uruguay"),
        ("UZB", "Uzbekistan"),
        ("VUT", "Vanuatu"),
        ("VAT", "Vatican City"),
        ("VEN", "Venezuela"),
        ("VNM", "Vietnam"),
        ("YEM", "Yemen"),
        ("ZMB", "Zambia"),
        ("ZWE", "Zimbabwe"),
    ]
    nationality = models.CharField(max_length=3, choices=NATIONALITY_CHOICES)
    speciality = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ["company_name"]
        indexes = [
            models.Index(fields=["company_name"]),
        ]
        verbose_name = "company"
        verbose_name_plural = "companies"


class Product(models.Model):
    p_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.FloatField()
    stock = models.IntegerField(default=0)
    discount = models.FloatField(
        default=0.0, validators=[MaxValueValidator(100.0), MinValueValidator(0.0)]
    )
    manfacture_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=False, blank=False)
    p_image = models.ImageField(upload_to="products/", blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_DEFAULT, null=True, default=1
    )
    cat = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    total_users_purchased = models.PositiveIntegerField(default=0)
    users_purchased_last_24_hours = models.PositiveIntegerField(default=0)
    last_purchase_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["product_name"]
        indexes = [
            models.Index(fields=["p_id", "slug"]),
            models.Index(fields=["product_name"]),
        ]

    def cal_discount(self):
        return self.price * (1 - self.discount)

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.p_id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


@receiver(signals.post_save, sender=Product)
@receiver(signals.post_delete, sender=Product)
def update_category_product_count(sender, instance, **kwargs):
    """
    Signal handler to update the product_count of the associated category when a product is saved or deleted.
    """
    category = instance.cat
    if category:
        category.product_count = category.product_set.count()
        category.save()
        parent_category = category.parent_cat
        while parent_category:
            parent_category.product_count = parent_category.product_set.aggregate(
                Sum("product_count")
            )["product_count__sum"]
            parent_category.save()
