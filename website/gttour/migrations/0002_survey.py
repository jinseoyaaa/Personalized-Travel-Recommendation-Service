# Generated by Django 4.2.3 on 2023-07-18 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gttour', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', '남'), ('F', '여')], max_length=1)),
                ('age', models.CharField(choices=[('1', '10대'), ('2', '20대'), ('3', '30대'), ('4', '40대'), ('5', '50대'), ('6', '60대 이상')], max_length=1)),
                ('region_1', models.CharField(choices=[('서울특별시', '서울특별시'), ('경기도', '경기도'), ('인천광역시', '인천광역시'), ('강원도', '강원도')], max_length=30)),
                ('area_1', models.CharField(choices=[('강남구', '강남구'), ('성동구', '성동구'), ('종로구', '종로구')], max_length=30)),
                ('region_2', models.CharField(blank=True, choices=[('서울특별시', '서울특별시'), ('경기도', '경기도'), ('인천광역시', '인천광역시'), ('강원도', '강원도')], max_length=30)),
                ('area_2', models.CharField(blank=True, choices=[('강남구', '강남구'), ('성동구', '성동구'), ('종로구', '종로구')], max_length=30)),
                ('region_3', models.CharField(blank=True, choices=[('서울특별시', '서울특별시'), ('경기도', '경기도'), ('인천광역시', '인천광역시'), ('강원도', '강원도')], max_length=30)),
                ('area_3', models.CharField(blank=True, choices=[('강남구', '강남구'), ('성동구', '성동구'), ('종로구', '종로구')], max_length=30)),
                ('myarea_1', models.CharField(max_length=60)),
                ('myarea_2', models.CharField(blank=True, max_length=60)),
                ('myarea_3', models.CharField(blank=True, max_length=60)),
            ],
        ),
    ]
