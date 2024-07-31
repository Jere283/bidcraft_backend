# Generated by Django 5.0.6 on 2024-07-28 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_favorites'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionImage',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image_url', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'auction_images',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuctionsTags',
            fields=[
                ('auction_tags_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auctions_tags',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tags',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Bids',
        ),
    ]
