# Generated by Django 3.2.12 on 2022-02-06 13:34

from django.db import migrations, models
import django.db.models.deletion
import input_types.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('executions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enumeration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('reported_to_defectdojo', models.BooleanField(default=False)),
                ('port', models.IntegerField()),
                ('port_status', models.TextField(choices=[('Open', 'Open'), ('Open - Filtered', 'Open Filtered'), ('Filtered', 'Filtered'), ('Closed', 'Closed')], default='Open', max_length=15)),
                ('protocol', models.TextField(blank=True, choices=[('UDP', 'Udp'), ('TCP', 'Tcp')], max_length=5, null=True)),
                ('service', models.TextField(blank=True, max_length=50, null=True)),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enumeration', to='executions.execution')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(models.Model, input_types.base.BaseInput),
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('reported_to_defectdojo', models.BooleanField(default=False)),
                ('name', models.TextField(max_length=100)),
                ('version', models.TextField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('reference', models.TextField(blank=True, max_length=250, null=True)),
                ('enumeration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='technology', to='findings.enumeration')),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='technology', to='executions.execution')),
                ('related_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='related_technologies', to='findings.technology')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(models.Model, input_types.base.BaseInput),
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('reported_to_defectdojo', models.BooleanField(default=False)),
                ('name', models.TextField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('severity', models.TextField(choices=[('Info', 'Info'), ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Critical', 'Critical')], default='Medium')),
                ('cve', models.TextField(blank=True, max_length=20, null=True)),
                ('cwe', models.TextField(blank=True, max_length=20, null=True)),
                ('osvdb', models.TextField(blank=True, max_length=20, null=True)),
                ('reference', models.TextField(blank=True, max_length=250, null=True)),
                ('enumeration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vulnerability', to='findings.enumeration')),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vulnerability', to='executions.execution')),
                ('technology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vulnerability', to='findings.technology')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(models.Model, input_types.base.BaseInput),
        ),
        migrations.CreateModel(
            name='OSINT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('reported_to_defectdojo', models.BooleanField(default=False)),
                ('data', models.TextField(max_length=250)),
                ('data_type', models.TextField(choices=[('IP', 'Ip'), ('Domain', 'Domain'), ('Url', 'Url'), ('Email', 'Email'), ('Link', 'Link'), ('ASN', 'Asn'), ('Username', 'User'), ('Password', 'Password')], max_length=10)),
                ('source', models.TextField(blank=True, max_length=50, null=True)),
                ('reference', models.TextField(blank=True, max_length=250, null=True)),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='osint', to='executions.execution')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(models.Model, input_types.base.BaseInput),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('reported_to_defectdojo', models.BooleanField(default=False)),
                ('address', models.TextField(max_length=30)),
                ('os', models.TextField(blank=True, max_length=250, null=True)),
                ('os_type', models.TextField(choices=[('Linux', 'Linux'), ('Windows', 'Windows'), ('MacOS', 'Macos'), ('iOS', 'Ios'), ('Android', 'Android'), ('Solaris', 'Solaris'), ('FreeBSD', 'Freebsd'), ('Other', 'Other')], default='Other', max_length=10)),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host', to='executions.execution')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(models.Model, input_types.base.BaseInput),
        ),
        migrations.CreateModel(
            name='Exploit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('reported_to_defectdojo', models.BooleanField(default=False)),
                ('name', models.TextField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('reference', models.TextField(blank=True, max_length=250, null=True)),
                ('checked', models.BooleanField(default=False)),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exploit', to='executions.execution')),
                ('technology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='exploit', to='findings.technology')),
                ('vulnerability', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='exploit', to='findings.vulnerability')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(models.Model, input_types.base.BaseInput),
        ),
        migrations.AddField(
            model_name='enumeration',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='enumeration', to='findings.host'),
        ),
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('reported_to_defectdojo', models.BooleanField(default=False)),
                ('endpoint', models.TextField(max_length=500)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('enumeration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='endpoint', to='findings.enumeration')),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endpoint', to='executions.execution')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(models.Model, input_types.base.BaseInput),
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('reported_to_defectdojo', models.BooleanField(default=False)),
                ('email', models.TextField(blank=True, max_length=100, null=True)),
                ('username', models.TextField(blank=True, max_length=100, null=True)),
                ('secret', models.TextField(blank=True, max_length=300, null=True)),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credential', to='executions.execution')),
                ('technology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='technology', to='findings.technology')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
            bases=(models.Model, input_types.base.BaseInput),
        ),
    ]
