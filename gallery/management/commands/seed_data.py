from django.core.management.base import BaseCommand
from faker import Faker
from gallery.models import Artist, Artwork, Event
import random
import requests
from django.core.files.base import ContentFile

fake = Faker('hr_HR')

PREDETERMINED_ARTWORKS = [
    {
        'title': 'Zvjezdana noć',
        'artist_name': 'Vincent van Gogh',
        'artist_nationality': 'Nizozemska',
        'artist_birth_year': 1853,
        'artist_bio': 'Vincent Willem van Gogh bio je nizozemski postimpresionistički slikar čiji rad je imao dalekosežan utjecaj na slikarstvo 20. stoljeća.',
        'artist_image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project_%28454045%29.jpg/800px-Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project_%28454045%29.jpg',
        'medium': 'oil',
        'year': 1889,
        'description': 'Zvjezdana noć prikazuje pogled iz prozora sobe Saint-Paul-de-Mausole azila prema selu Saint-Rémy-de-Provence, tik prije izlaska sunca.',
        'price': 0,
        'is_available': False,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg',
    },
    {
        'title': 'Mona Lisa',
        'artist_name': 'Leonardo da Vinci',
        'artist_nationality': 'Italija',
        'artist_birth_year': 1452,
        'artist_bio': 'Leonardo di ser Piero da Vinci bio je talijanski renesansni polimatt čije su se zanimanje, otkrića i umijeće protezala na brojna područja.',
        'artist_image_url': 'https://www.leonardodavinci.net/assets/img/leonardo-da-vinci.jpg',
        'medium':'oil',
        'year': 1503,
        'description': 'Mona Lisa je portret uljenim bojama na drvenoj ploči talijanskog umjetnika Leonarda da Vincija. Jedan je od najpoznatijih i najposjećenijih umjetničkih djela na svijetu.',
        'price': 0,
        'is_available': False,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6a/Mona_Lisa.jpg',
    },
    {
        'title': 'Djevojka s bisernom naušnicom',
        'artist_name': 'Johannes Vermeer',
        'artist_nationality': 'Nizozemska',
        'artist_birth_year': 1632,
        'artist_bio': 'Johannes Vermeer bio je nizozemski barokni slikar koji je djelovao u Delftu. Poznat je po majstorskom prikazivanju svjetlosti u interijerima.',
        'artist_image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Johannes_Vermeer_-_Van_Gogh_Museum.jpg/800px-Johannes_Vermeer_-_Van_Gogh_Museum.jpg',
        'medium': 'oil',
        'year': 1665,
        'description': 'Djevojka s bisernom naušnicom jedan je od najpoznatijih nizozemskih zlatnog doba slikarstva. Prikazuje djevojku u egzotičnoj odjeći s velikom bisernom naušnicom.',
        'price': 0,
        'is_available': False,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/d/d7/Meisje_met_de_parel.jpg',
    },
    {
        'title': 'Veliki val kod Kanagawe',
        'artist_name': 'Katsushika Hokusai',
        'artist_nationality': 'Japan',
        'artist_birth_year': 1760,
        'artist_bio': 'Katsushika Hokusai bio je japanski umjetnik, grafičar i slikar ere Edo. Jedan je od najutjecajnijih japanskih umjetnika u povijesti.',
        'artist_image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Katsushika_Hokusai.jpg/800px-Katsushika_Hokusai.jpg',
        'medium': 'photography',
        'year': 1831,
        'description': 'Veliki val kod Kanagawe je drvorez japanskog umjetnika Hokusaija. Prikazuje veliki val koji prijeti čamcima ispred planine Fuji.',
        'price': 0,
        'is_available': False,
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/1280px-Tsunami_by_hokusai_19th_century.jpg',
    },
]


def download_image(url, filename):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code == 200:
            return ContentFile(response.content), filename
    except Exception as e:
        print(f'  Greška pri preuzimanju slike: {e}')
    return None, None


class Command(BaseCommand):
    help = 'Generiraj testne podatke'

    def handle(self, *args, **kwargs):
        Event.objects.all().delete()
        Artwork.objects.all().delete()
        Artist.objects.all().delete()

        self.stdout.write('Kreiram predetermined djela i umjetnike...')

        predetermined_artworks = []
        for data in PREDETERMINED_ARTWORKS:
            artist, _ = Artist.objects.get_or_create(
                name=data['artist_name'],
                defaults={
                    'bio': data['artist_bio'],
                    'nationality': data['artist_nationality'],
                    'birth_year': data['artist_birth_year'],
                }
            )

            if not artist.image and data.get('artist_image_url'):
                self.stdout.write(f'  Preuzimam sliku za umjetnika: {data["artist_name"]}...')
                image_content, filename = download_image(
                    data['artist_image_url'],
                    f"{data['artist_name'].replace(' ', '_')}.jpg"
                )
                if image_content:
                    artist.image.save(filename, image_content, save=True)
                    self.stdout.write(f'  Slika spremljena za: {data["artist_name"]}')
                else:
                    self.stdout.write(f'  Nije moguće preuzeti sliku za: {data["artist_name"]}')

            artwork = Artwork.objects.create(
                title=data['title'],
                artist=artist,
                medium=data['medium'],
                year=data['year'],
                description=data['description'],
                price=data['price'],
                is_available=data['is_available'],
            )

            self.stdout.write(f'  Preuzimam sliku za djelo: {data["title"]}...')
            image_content, filename = download_image(
                data['image_url'],
                f"{data['title'].replace(' ', '_')}.jpg"
            )
            if image_content:
                artwork.image.save(filename, image_content, save=True)
                self.stdout.write(f'  Slika spremljena za djelo: {data["title"]}')
            else:
                self.stdout.write(f'  Nije moguće preuzeti sliku za djelo: {data["title"]}')

            predetermined_artworks.append(artwork)

        self.stdout.write('Kreiram random umjetnike i djela...')

        random_artists = []
        for _ in range(6):
            a = Artist.objects.create(
                name=fake.name(),
                bio=fake.paragraph(nb_sentences=4),
                nationality=fake.country(),
                birth_year=random.randint(1940, 1995),
                website=fake.url(),
            )
            random_artists.append(a)

        mediums = ['oil', 'watercolor', 'digital', 'sculpture', 'photography']
        random_artworks = []
        for _ in range(6):
            aw = Artwork.objects.create(
                title=fake.catch_phrase(),
                artist=random.choice(random_artists),
                medium=random.choice(mediums),
                year=random.randint(1990, 2024),
                description=fake.paragraph(nb_sentences=3),
                price=round(random.uniform(100, 10000), 2),
                is_available=random.choice([True, False]),
            )
            random_artworks.append(aw)

        self.stdout.write('Kreiram događanja...')

        all_artworks = predetermined_artworks + random_artworks
        event_types = ['exhibition', 'workshop', 'lecture', 'concert']
        event_names = [
            'Otvorenje proljetne izložbe',
            'Radionica akvarela za početnike',
            'Predavanje o suvremenoj umjetnosti',
            'Večer klasične glazbe i slikarstva',
        ]

        for i in range(4):
            ev = Event.objects.create(
                title=event_names[i],
                event_type=event_types[i],
                description=fake.paragraph(nb_sentences=3),
                location=fake.address(),
                date=fake.date_between(start_date='today', end_date='+1y'),
                start_time=fake.time(),
                capacity=random.randint(20, 200),
                is_free=random.choice([True, False]),
            )
            ev.artworks.set(random.sample(all_artworks, k=random.randint(2, 5)))

        self.stdout.write(self.style.SUCCESS(
            f'Gotovo! Kreirano: {len(PREDETERMINED_ARTWORKS)} predetermined + 6 random djela, 4 događanja.'
        ))