# Tells Django's migration state that `slug` exists (it's already a real
# column in the database from an earlier partial migration run), then
# adds the unique constraint for real.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_remove_servicecard_cta_url_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='servicecard',
                    name='slug',
                    field=models.SlugField(blank=True, max_length=160),
                ),
            ],
            database_operations=[],
        ),
        migrations.AlterField(
            model_name='servicecard',
            name='slug',
            field=models.SlugField(blank=True, max_length=160, unique=True),
        ),
    ]