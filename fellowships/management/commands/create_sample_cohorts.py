from django.core.management.base import BaseCommand
from fellowships.models import Cohort, Fellow, CohortProject, CohortEvent, CohortGalleryImage
from datetime import date


class Command(BaseCommand):
    help = 'Create sample fellowship cohorts for 2024 and 2025'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample cohorts...')

        # Create 2025 Cohort
        cohort_2025, created = Cohort.objects.get_or_create(
            slug='2025-cohort',
            defaults={
                'name': '2025 Cohort',
                'year': 2025,
                'overview': '''The 2025 Fellowship Cohort brings together emerging leaders and researchers committed to strengthening governance and democracy in East Africa. This year's cohort focuses on policy innovation, community engagement, and evidence-based research to address pressing governance challenges.

Our fellows will work on cutting-edge projects spanning electoral reform, public accountability, civic engagement, and regional policy coordination. Through mentorship, collaborative research, and practical field experience, fellows develop the skills and networks needed to drive meaningful change in their communities and beyond.''',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created cohort: {cohort_2025.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Cohort already exists: {cohort_2025.name}'))

        # Create Fellows for 2025
        fellows_2025 = [
            {
                'name': 'Amina Nakato',
                'bio': 'Policy researcher focusing on electoral systems and democratic governance. Passionate about youth participation in politics.',
                'position': 'Research Fellow',
            },
            {
                'name': 'David Ochieng',
                'bio': 'Community organizer with experience in civic education and grassroots mobilization across rural Uganda.',
                'position': 'Community Fellow',
            },
            {
                'name': 'Sarah Kamau',
                'bio': 'Data analyst specializing in public finance transparency and budget monitoring in East Africa.',
                'position': 'Research Fellow',
            },
            {
                'name': 'James Mwangi',
                'bio': 'Regional policy expert working on cross-border governance issues and East African Community integration.',
                'position': 'Regional Fellow',
            },
            {
                'name': 'Grace Akinyi',
                'bio': 'Gender and governance specialist with a focus on women\'s political participation and leadership development.',
                'position': 'Leadership Fellow',
            },
        ]

        for fellow_data in fellows_2025:
            fellow, created = Fellow.objects.get_or_create(
                cohort=cohort_2025,
                name=fellow_data['name'],
                defaults={
                    'bio': fellow_data['bio'],
                    'position': fellow_data['position'],
                }
            )
            if created:
                self.stdout.write(f'  - Created fellow: {fellow.name}')

        # Create Projects for 2025
        projects_2025 = [
            {
                'title': 'Youth Electoral Participation Study',
                'description': 'Comprehensive research on barriers to youth voter registration and participation in Uganda\'s electoral process.',
            },
            {
                'title': 'Community Budget Monitoring Initiative',
                'description': 'Training and supporting community groups to monitor local government budget implementation and service delivery.',
            },
            {
                'title': 'Regional Policy Harmonization Framework',
                'description': 'Analysis and recommendations for harmonizing governance policies across East African Community member states.',
            },
        ]

        for project_data in projects_2025:
            project, created = CohortProject.objects.get_or_create(
                cohort=cohort_2025,
                title=project_data['title'],
                defaults={
                    'description': project_data['description'],
                }
            )
            if created:
                self.stdout.write(f'  - Created project: {project.title}')

        # Create Events for 2025
        events_2025 = [
            {
                'title': 'Cohort Launch & Orientation',
                'description': 'Official launch event bringing together all 2025 fellows, mentors, and CEPA staff for orientation and networking.',
                'event_date': date(2025, 2, 15),
                'location': 'CEPA Office, Kampala',
            },
            {
                'title': 'Research Methodology Workshop',
                'description': 'Intensive training on qualitative and quantitative research methods for policy analysis.',
                'event_date': date(2025, 3, 10),
                'location': 'Makerere University, Kampala',
            },
            {
                'title': 'Mid-Year Review & Presentations',
                'description': 'Fellows present their research progress and receive feedback from peers and senior researchers.',
                'event_date': date(2025, 7, 20),
                'location': 'CEPA Office, Kampala',
            },
            {
                'title': 'Regional Policy Forum',
                'description': 'Cross-border dialogue bringing together fellows, policymakers, and civil society from across East Africa.',
                'event_date': date(2025, 9, 5),
                'location': 'Nairobi, Kenya',
            },
        ]

        for event_data in events_2025:
            event, created = CohortEvent.objects.get_or_create(
                cohort=cohort_2025,
                title=event_data['title'],
                defaults={
                    'description': event_data['description'],
                    'event_date': event_data['event_date'],
                    'location': event_data['location'],
                }
            )
            if created:
                self.stdout.write(f'  - Created event: {event.title}')

        # Create 2024 Cohort
        cohort_2024, created = Cohort.objects.get_or_create(
            slug='2024-cohort',
            defaults={
                'name': '2024 Cohort',
                'year': 2024,
                'overview': '''The 2024 Fellowship Cohort marked a milestone year for CEPA's fellowship program, bringing together 6 exceptional fellows from across East Africa. This cohort focused on strengthening democratic institutions, enhancing public accountability, and promoting citizen engagement in governance processes.

Throughout the year, our fellows conducted groundbreaking research on electoral integrity, local governance, and civic participation. They worked closely with communities, government officials, and civil society organizations to develop evidence-based policy recommendations that have already begun influencing governance reforms in the region.''',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created cohort: {cohort_2024.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Cohort already exists: {cohort_2024.name}'))

        # Create Fellows for 2024
        fellows_2024 = [
            {
                'name': 'Peter Mugisha',
                'bio': 'Electoral systems expert with 5 years experience monitoring elections across East Africa. Led research on voter behavior patterns.',
                'position': 'Research Fellow',
            },
            {
                'name': 'Rebecca Auma',
                'bio': 'Local governance specialist focusing on decentralization and community participation in public decision-making.',
                'position': 'Community Fellow',
            },
            {
                'name': 'John Kiprotich',
                'bio': 'Public accountability researcher examining oversight mechanisms and anti-corruption initiatives in local government.',
                'position': 'Research Fellow',
            },
            {
                'name': 'Mary Namuganza',
                'bio': 'Communications strategist working to increase civic awareness and political literacy among marginalized communities.',
                'position': 'Community Fellow',
            },
            {
                'name': 'Hassan Juma',
                'bio': 'Regional integration expert analyzing policy coordination and harmonization across EAC member states.',
                'position': 'Regional Fellow',
            },
            {
                'name': 'Christine Wanjiru',
                'bio': 'Veteran civil society leader with 10 years experience in advocacy, policy research, and governance programming.',
                'position': 'Leadership Fellow',
            },
        ]

        for fellow_data in fellows_2024:
            fellow, created = Fellow.objects.get_or_create(
                cohort=cohort_2024,
                name=fellow_data['name'],
                defaults={
                    'bio': fellow_data['bio'],
                    'position': fellow_data['position'],
                }
            )
            if created:
                self.stdout.write(f'  - Created fellow: {fellow.name}')

        # Create Projects for 2024
        projects_2024 = [
            {
                'title': 'Electoral Integrity Assessment',
                'description': 'Comprehensive study of electoral processes and integrity mechanisms in Uganda\'s 2024 local government elections.',
            },
            {
                'title': 'Civic Engagement Platform',
                'description': 'Development of digital tools and resources to enhance citizen participation in local governance and budget monitoring.',
            },
            {
                'title': 'Anti-Corruption Watchdog Network',
                'description': 'Establishment of community-based monitoring groups to track public procurement and service delivery.',
            },
            {
                'title': 'Policy Brief Series on Decentralization',
                'description': 'Research-based policy recommendations for strengthening local government autonomy and accountability.',
            },
        ]

        for project_data in projects_2024:
            project, created = CohortProject.objects.get_or_create(
                cohort=cohort_2024,
                title=project_data['title'],
                defaults={
                    'description': project_data['description'],
                }
            )
            if created:
                self.stdout.write(f'  - Created project: {project.title}')

        # Create Events for 2024
        events_2024 = [
            {
                'title': 'Fellowship Induction Ceremony',
                'description': 'Welcome event for the 2024 cohort featuring keynote address by prominent governance expert.',
                'event_date': date(2024, 1, 20),
                'location': 'CEPA Office, Kampala',
            },
            {
                'title': 'Field Research Training',
                'description': 'Hands-on training in field research techniques, data collection, and community engagement methods.',
                'event_date': date(2024, 3, 15),
                'location': 'Gulu, Uganda',
            },
            {
                'title': 'Interim Research Presentations',
                'description': 'Fellows share preliminary findings from their research projects and receive peer feedback.',
                'event_date': date(2024, 6, 25),
                'location': 'CEPA Office, Kampala',
            },
            {
                'title': 'East Africa Governance Summit',
                'description': 'Regional conference where fellows presented research findings to policymakers and practitioners.',
                'event_date': date(2024, 10, 10),
                'location': 'Dar es Salaam, Tanzania',
            },
            {
                'title': 'Fellowship Graduation & Awards',
                'description': 'Celebration of cohort achievements with presentation of final research outputs and awards ceremony.',
                'event_date': date(2024, 12, 15),
                'location': 'CEPA Office, Kampala',
            },
        ]

        for event_data in events_2024:
            event, created = CohortEvent.objects.get_or_create(
                cohort=cohort_2024,
                title=event_data['title'],
                defaults={
                    'description': event_data['description'],
                    'event_date': event_data['event_date'],
                    'location': event_data['location'],
                }
            )
            if created:
                self.stdout.write(f'  - Created event: {event.title}')

        self.stdout.write(self.style.SUCCESS('\nSample cohorts created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Total cohorts: {Cohort.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total fellows: {Fellow.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total projects: {CohortProject.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total events: {CohortEvent.objects.count()}'))
