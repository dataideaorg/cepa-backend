from django.core.management.base import BaseCommand
from resources.models import BlogPost, NewsArticle, Publication, Event


class Command(BaseCommand):
    help = 'Populate the database with existing hardcoded data from frontend'

    def handle(self, *args, **options):
        self.stdout.write('Starting data population...')
        
        # Blog Posts Data
        blog_posts_data = [
            {
                'id': 'education-are-we-doing-good-job-children',
                'title': 'Education: Are we doing a good job with our children?',
                'date': 'February 2022',
                'category': 'Education',
                'description': 'An analysis of Uganda\'s education sector challenges, particularly the impact of COVID-19 lockdowns on learners and the need for increased government investment in education.',
                'image': '/blog/education-children.jpg',
                'slug': 'education-are-we-doing-a-good-job-with-our-children',
                'featured': True
            },
            {
                'id': 'parliament-approving-decisions-wrong-reasons',
                'title': 'Parliament Approving Decisions for all the Wrong Reasons',
                'date': 'March 2022',
                'category': 'Governance',
                'description': 'A critical examination of parliamentary decision-making processes and the need for more evidence-based policy formulation in Uganda\'s legislative body.',
                'image': '/blog/parliament-decisions.jpg',
                'slug': 'parliament-approving-decisions-for-all-the-wrong-reasons',
                'featured': True
            },
            {
                'id': 'data-protection-digital-age-analysis',
                'title': 'Data Protection in the Digital Age: An Analysis of Uganda\'s Data Protection and Privacy Bill 2015',
                'date': 'April 2022',
                'category': 'Digital Rights',
                'description': 'Comprehensive analysis of Uganda\'s proposed data protection legislation and its implications for digital rights, privacy, and cybersecurity in the country.',
                'image': '/blog/data-protection.jpg',
                'slug': 'data-protection-in-the-digital-age-an-analysis-of-ugandas-data-protection-and-privacy-bill-2015',
                'featured': True
            },
            {
                'id': 'road-safety-uganda-comprehensive-regulations',
                'title': 'Road Safety in Uganda: Why Uganda Needs Comprehensive Regulations for Road Users',
                'date': 'May 2022',
                'category': 'Road Safety',
                'description': 'Analysis of road safety challenges in Uganda and recommendations for comprehensive regulatory framework to reduce traffic accidents and fatalities.',
                'image': '/blog/road-safety-regulations.jpg',
                'slug': 'road-safety-in-uganda-why-uganda-needs-comprehensive-regulations-for-road-users',
                'featured': False
            },
            {
                'id': 'parliamentary-oversight-accountability-service-delivery',
                'title': 'Parliamentary Oversight in Accountability Affects Service Delivery in Public Institutions',
                'date': 'June 2022',
                'category': 'Governance',
                'description': 'Examination of how effective parliamentary oversight mechanisms can improve accountability and service delivery in Uganda\'s public institutions.',
                'image': '/blog/parliamentary-oversight.jpg',
                'slug': 'parliamentary-oversight-in-accountability-affects-service-delivery-in-public-institutions',
                'featured': False
            },
            {
                'id': 'health-sector-resources-properly',
                'title': 'Health Sector: We are still not using the little resources allocated properly',
                'date': 'July 2022',
                'category': 'Health',
                'description': 'Critical analysis of resource allocation and utilization in Uganda\'s health sector, highlighting inefficiencies and recommendations for improvement.',
                'image': '/blog/health-sector-resources.jpg',
                'slug': 'health-sector-we-are-still-not-using-the-little-resources-allocated-properly',
                'featured': False
            },
            {
                'id': 'affirmative-action-youth-misunderstood',
                'title': 'Affirmative Action to the Youth was Misunderstood: Can we do better?',
                'date': 'August 2022',
                'category': 'Youth',
                'description': 'Analysis of youth affirmative action policies in Uganda, examining their effectiveness and proposing better approaches to youth empowerment.',
                'image': '/blog/youth-affirmative-action.jpg',
                'slug': 'affirmative-action-to-the-youth-was-misunderstood-can-we-do-better',
                'featured': False
            },
            {
                'id': 'budget-framework-paper-young-peoples-interests',
                'title': 'Analysis of the 2020-2021 Budget Framework Paper: Where the Young People\'s Interests? A Look at ICT and Taxation',
                'date': 'September 2022',
                'category': 'Budget Analysis',
                'description': 'Detailed analysis of Uganda\'s budget framework paper focusing on youth interests, ICT development, and taxation policies affecting young people.',
                'image': '/blog/budget-framework-youth.jpg',
                'slug': 'analysis-of-the-2020-2021-budget-framework-paper-where-the-young-peoples-interests-a-look-at-ict-and-taxation',
                'featured': False
            },
            {
                'id': 'parliament-needs-change-loans-handling',
                'title': 'Parliament Needs to Change its Mode of Loans Handling',
                'date': 'October 2022',
                'category': 'Public Finance',
                'description': 'Analysis of parliamentary oversight of loan approvals and recommendations for improving transparency and accountability in debt management.',
                'image': '/blog/parliament-loans.jpg',
                'slug': 'parliament-needs-to-change-its-mode-of-loans-handling',
                'featured': False
            },
            {
                'id': 'reproductive-health-public-health-concern',
                'title': 'Reproductive Health is a Public Health Concern',
                'date': 'November 2022',
                'category': 'Health',
                'description': 'Examination of reproductive health challenges in Uganda and the need for comprehensive policies to address maternal and child health issues.',
                'image': '/blog/reproductive-health.jpg',
                'slug': 'reproductive-health-is-a-public-health-concern',
                'featured': False
            }
        ]

        # News Articles Data
        news_articles_data = [
            {
                'id': 'ministry-health-ugx450bn-emergency-services',
                'title': 'Ministry of Health Seeks UGX450Bn for Emergency Medical Services for Road Crash Victims',
                'date': 'September 2023',
                'category': 'Health',
                'description': 'The Ministry of Health has revealed that Uganda needs UGX450Bn over 5 years to purchase and operationalize ambulances to reduce road crash deaths. The call was made during an advocacy meeting organized by CEPA.',
                'image': '/news/health-emergency-services.jpg',
                'slug': 'ministry-of-health-seeks-ugx450bn-for-emergency-medical-services-for-road-crash-victims',
                'featured': True
            },
            {
                'id': 'world-remembrance-day-road-traffic-victims',
                'title': 'World Remembrance Day For Road Traffic Victims Should be a Day to Propel Action',
                'date': 'November 2023',
                'category': 'Road Safety',
                'description': 'As Uganda commemorates World Remembrance Day for Road Traffic Victims, CEPA calls for concrete action to address the growing road safety crisis and implement effective measures to reduce traffic-related deaths.',
                'image': '/news/road-safety-remembrance.jpg',
                'slug': 'world-remembrance-day-for-road-traffic-victims-should-be-a-day-to-propel-action',
                'featured': True
            },
            {
                'id': 'financing-safer-roads-stakeholders',
                'title': 'Financing Safer Roads: CEPA Rallies Stakeholders for Increased Road Safety Investment',
                'date': 'July 2025',
                'category': 'Road Safety',
                'description': 'CEPA convenes key stakeholders to discuss strategies for increasing investment in road safety infrastructure and programs across Uganda to reduce traffic accidents and fatalities.',
                'image': '/news/financing-safer-roads.jpg',
                'slug': 'financing-safer-roads-cepa-rallies-stakeholders-for-increased-road-safety-investment',
                'featured': True
            },
            {
                'id': 'parliamentary-committee-health-neapacoh',
                'title': '16th Network of African Parliamentary Committees of Health (NEAPACOH) Meeting',
                'date': 'July 2025',
                'category': 'Health',
                'description': 'CEPA participates in the 16th NEAPACOH meeting, contributing to regional discussions on health policy and parliamentary oversight to improve healthcare delivery across Africa.',
                'image': '/news/neapacoh-meeting.jpg',
                'slug': '16th-network-of-african-parliamentary-committees-of-health-neapacoh',
                'featured': False
            },
            {
                'id': 'road-safety-advocacy-continued',
                'title': 'Road Safety Advocacy: CEPA\'s Continued Commitment to Safer Roads',
                'date': 'July 2025',
                'category': 'Advocacy',
                'description': 'Ongoing advocacy efforts by CEPA to promote road safety policies and improve transportation infrastructure in Uganda through evidence-based research and stakeholder engagement.',
                'image': '/news/road-safety-advocacy.jpg',
                'slug': 'road-safety-advocacy',
                'featured': False
            },
            {
                'id': 'biotechnology-biosafety-uganda',
                'title': 'Biotechnology and Biosafety in Uganda: Utility in Transforming the Economy and Health Sector',
                'date': 'August 2023',
                'category': 'Health',
                'description': 'Analysis of Uganda\'s biotechnology and biosafety framework and its potential to transform the economy and health sector through innovative scientific solutions.',
                'image': '/news/biotechnology-biosafety.jpg',
                'slug': 'biotechnology-and-biosafety-in-uganda-utility-in-transforming-the-economy-and-health-sector',
                'featured': False
            },
            {
                'id': 'education-pregnant-students-rights',
                'title': 'Education: Uganda Registers Rights Progress for Pregnant Students but Barriers Remain',
                'date': 'June 2023',
                'category': 'Education',
                'description': 'While Uganda has made progress in protecting the rights of pregnant students to continue their education, significant barriers still exist that need to be addressed.',
                'image': '/news/education-pregnant-students.jpg',
                'slug': 'education-uganda-registers-rights-progress-for-pregnant-students-but-barriers-remain',
                'featured': False
            },
            {
                'id': 'national-road-safety-action-plan',
                'title': 'National Road Safety Action Plan 2022-2026',
                'date': 'March 2023',
                'category': 'Road Safety',
                'description': 'Analysis of Uganda\'s National Road Safety Action Plan 2022-2026 and its implementation strategies to reduce road traffic accidents and improve safety standards.',
                'image': '/news/national-road-safety-plan.jpg',
                'slug': 'national-road-safety-action-plan-2022-2026',
                'featured': False
            },
            {
                'id': 'parliamentary-pensions-amendment-bill',
                'title': 'Parliamentary Pensions Amendment Bill 2022',
                'date': 'February 2023',
                'category': 'Governance',
                'description': 'Analysis of the Parliamentary Pensions Amendment Bill 2022 and its implications for legislative accountability and pension management in Uganda.',
                'image': '/news/parliamentary-pensions-bill.jpg',
                'slug': 'parliamentary-pensions-amendment-bill-2022',
                'featured': False
            },
            {
                'id': 'computer-misuse-amendment-bill',
                'title': 'Computer Misuse Amendment Bill 2022',
                'date': 'August 2022',
                'category': 'Digital Rights',
                'description': 'Analysis of the Computer Misuse Amendment Bill 2022 and its implications for digital rights, freedom of expression, and cybersecurity in Uganda.',
                'image': '/news/computer-misuse-bill.jpg',
                'slug': 'computer-misuse-amendment-bill-2022',
                'featured': False
            }
        ]

        # Publications Data
        publications_data = [
            {
                'id': 'policy-brief-democratic-governance',
                'title': 'Policy Brief: Advancing Democratic Governance: Leveraging Digital Tools for Inclusive Parliamentary Monitoring in Africa and Beyond',
                'type': 'Policy Brief',
                'date': '2024',
                'description': 'This policy brief explores how digital tools can enhance parliamentary monitoring and democratic governance across Africa, providing recommendations for inclusive and effective oversight mechanisms.',
                'category': 'Governance',
                'url': 'https://cepa.or.ug/blogs/policy-brief-advancing-democratic-governance-leveraging-digital-tools-for-inclusive-parliamentary-monitoring-in-africa-and-beyond/',
                'pdf': '/publications/policy-brief-democratic-governance.pdf',
                'featured': True
            },
            {
                'id': 'budget-analysis-2024',
                'title': 'Policy Paper: Analyzing the Practicability and Sustainability of Uganda\'s FY2024-25 Budget: Challenges, Implications and Policy Recommendations',
                'type': 'Policy Paper',
                'date': '2024',
                'description': 'A comprehensive analysis of Uganda\'s 2024-25 budget framework, examining its sustainability and providing evidence-based policy recommendations for improved fiscal management.',
                'category': 'Public Finance',
                'url': 'https://cepa.or.ug/blogs/policy-paper-analyzing-the-practicability-and-sustainability-of-ugandas-fy2024-25-budget-challenges-implications-and-policy-recommendations/',
                'pdf': '/publications/policy-paper-budget-analysis.pdf',
                'featured': True
            },
            {
                'id': 'access-information-press-freedom',
                'title': 'Policy Paper: Strengthening Access to Information and Press Freedom in Uganda: Policy Recommendations for Enhancing Transparency, Accountability and Citizen Participation',
                'type': 'Policy Paper',
                'date': '2024',
                'description': 'This policy paper examines the current state of access to information and press freedom in Uganda, offering strategic recommendations to enhance transparency and citizen participation in governance.',
                'category': 'Transparency',
                'url': 'https://cepa.or.ug/blogs/policy-paper-strengthening-access-to-information-and-press-freedom-in-uganda-policy-recommendations-for-enhancing-transparency-accountability-and-citizen-participation/',
                'pdf': '/publications/policy-paper-press-freedom.pdf',
                'featured': True
            },
            {
                'id': 'data-protection-analysis',
                'title': 'Data Protection in the Digital Age: An Analysis of Uganda\'s Data Protection and Privacy Bill 2015',
                'type': 'Analysis',
                'date': '2015',
                'description': 'Comprehensive analysis of Uganda\'s Data Protection and Privacy Bill, examining its provisions and implications for digital rights and privacy protection.',
                'category': 'Digital Rights',
                'url': 'https://cepa.or.ug/blogs/data-protection-in-the-digital-age-an-analysis-of-ugandas-data-protection-and-privacy-bill-2015/',
                'pdf': None,
                'featured': False
            },
            {
                'id': 'children-amendment-bill',
                'title': 'An Analytical Overview of Uganda\'s Proposed Children Amendment Bill 2015',
                'type': 'Analysis',
                'date': '2015',
                'description': 'Detailed analysis of the Children Amendment Bill 2015, focusing on its potential impact on child rights and protection in Uganda.',
                'category': 'Human Rights',
                'url': 'https://cepa.or.ug/blogs/an-analytical-overview-of-ugandas-proposed-children-amendment-bill-2015/',
                'pdf': '/publications/children-amendment-bill-analysis.pdf',
                'featured': False
            },
            {
                'id': 'tobacco-control-bill',
                'title': 'Comprehensive Ban on Tobacco Advertising in the Recently Passed Tobacco Control Bill is Within Public Interest',
                'type': 'Analysis',
                'date': '2024',
                'description': 'Analysis of the Tobacco Control Bill\'s advertising restrictions, arguing for their alignment with public health interests and constitutional rights.',
                'category': 'Public Health',
                'url': 'https://cepa.or.ug/blogs/comprehensive-ban-on-tobacco-advertising-in-the-recently-passed-tobbaco-control-bill-is-within-public-interest-and-does-not-infringe-tobacco-companies-intellectual-property-rights/',
                'pdf': '/publications/tobacco-control-bill-analysis.pdf',
                'featured': False
            }
        ]

        # Events Data
        events_data = [
            {
                'id': 'uganda-road-safety-conference-2025',
                'title': 'Driving Policy into Action: CEPA Co-Convenes the 2025 Uganda Road Safety Conference',
                'date': 'May 14-15, 2025',
                'time': '9:00 AM - 5:00 PM',
                'location': 'Kampala, Uganda',
                'category': 'Conference',
                'description': 'From 14–15 May 2025, CEPA co-convened the Uganda Road Safety Conference, bringing together policymakers, civil society organizations, and road safety experts to discuss innovative approaches to reducing road traffic accidents and fatalities in Uganda.',
                'image': '/events/road-safety-conference.jpg',
                'slug': 'uganda-road-safety-conference-2025',
                'featured': True,
                'status': 'upcoming'
            },
            {
                'id': 'neapacoh-meeting-tanzania-2025',
                'title': 'Championing SRHR through Legislative Engagement: CEPA at the 16th NEAPACOH Meeting in Tanzania',
                'date': 'March 5-8, 2025',
                'time': '8:00 AM - 6:00 PM',
                'location': 'Dar es Salaam, Tanzania',
                'category': 'Meeting',
                'description': 'CEPA participated in the 16th NEAPACOH meeting from 5th to 8th March 2025, focusing on sexual and reproductive health rights (SRHR) advocacy and legislative engagement across East and Central Africa.',
                'image': '/events/neapacoh-meeting.jpg',
                'slug': 'neapacoh-meeting-tanzania-2025',
                'featured': True,
                'status': 'upcoming'
            },
            {
                'id': 'ethiopia-civil-society-workshop-2024',
                'title': 'Bridging Borders, Deepening Democracy: CEPA\'s Experience-Sharing at the Ethiopia Civil Society Engagement Workshop',
                'date': 'November 19, 2024',
                'time': '9:00 AM - 4:00 PM',
                'location': 'Addis Ababa, Ethiopia',
                'category': 'Workshop',
                'description': 'CEPA joined regional civil society leaders in Ethiopia for a comprehensive workshop on democratic engagement, policy advocacy, and cross-border collaboration in East Africa.',
                'image': '/events/ethiopia-workshop.jpg',
                'slug': 'ethiopia-civil-society-workshop-2024',
                'featured': False,
                'status': 'completed'
            },
            {
                'id': 'africa-road-safety-seminar-2024',
                'title': 'The Africa Road Safety Seminar 2024 in Nairobi, Kenya',
                'date': 'October 21, 2024',
                'time': '8:30 AM - 5:30 PM',
                'location': 'Nairobi, Kenya',
                'category': 'Seminar',
                'description': 'Being half way through the African Road Safety Action Plan, this seminar brought together road safety stakeholders from across the continent to assess progress and chart the way forward for safer roads in Africa.',
                'image': '/events/africa-road-safety-seminar.jpg',
                'slug': 'africa-road-safety-seminar-2024',
                'featured': False,
                'status': 'completed'
            },
            {
                'id': 'speed-management-validation-meetings-2024',
                'title': 'Speed Management in Uganda: Insights from the validation meetings on the speed regulations',
                'date': 'August 5, 2024',
                'time': '10:00 AM - 3:00 PM',
                'location': 'Kampala, Uganda',
                'category': 'Validation Meeting',
                'description': 'In an effort to strengthen the road safety policy framework, CEPA facilitated validation meetings to review and refine speed management regulations for Uganda\'s road network.',
                'image': '/events/speed-management-meeting.jpg',
                'slug': 'speed-management-validation-meetings-2024',
                'featured': False,
                'status': 'completed'
            },
            {
                'id': 'youth-policy-advocacy-training-2024',
                'title': 'Youth Policy Advocacy Training Workshop',
                'date': 'July 15-17, 2024',
                'time': '9:00 AM - 4:00 PM',
                'location': 'Kampala, Uganda',
                'category': 'Training',
                'description': 'A comprehensive training program designed to equip young people with the skills and knowledge needed to effectively engage in policy advocacy and legislative processes.',
                'image': '/events/youth-training.jpg',
                'slug': 'youth-policy-advocacy-training-2024',
                'featured': False,
                'status': 'completed'
            },
            {
                'id': 'parliamentary-oversight-seminar-2024',
                'title': 'Strengthening Parliamentary Oversight: A Regional Seminar',
                'date': 'June 10-12, 2024',
                'time': '8:30 AM - 5:00 PM',
                'location': 'Kampala, Uganda',
                'category': 'Seminar',
                'description': 'This regional seminar brought together parliamentarians and civil society representatives to discuss best practices in parliamentary oversight and accountability mechanisms.',
                'image': '/events/parliamentary-oversight.jpg',
                'slug': 'parliamentary-oversight-seminar-2024',
                'featured': False,
                'status': 'completed'
            },
            {
                'id': 'digital-rights-conference-2024',
                'title': 'Digital Rights and Data Protection Conference 2024',
                'date': 'May 20-22, 2024',
                'time': '9:00 AM - 6:00 PM',
                'location': 'Kampala, Uganda',
                'category': 'Conference',
                'description': 'A comprehensive conference exploring digital rights, data protection, and cybersecurity challenges in Uganda and the broader East African region.',
                'image': '/events/digital-rights-conference.jpg',
                'slug': 'digital-rights-conference-2024',
                'featured': False,
                'status': 'completed'
            }
        ]

        # Create Blog Posts
        self.stdout.write('Creating blog posts...')
        for post_data in blog_posts_data:
            BlogPost.objects.get_or_create(
                id=post_data['id'],
                defaults=post_data
            )
        self.stdout.write(f'Created {len(blog_posts_data)} blog posts')

        # Create News Articles
        self.stdout.write('Creating news articles...')
        for article_data in news_articles_data:
            NewsArticle.objects.get_or_create(
                id=article_data['id'],
                defaults=article_data
            )
        self.stdout.write(f'Created {len(news_articles_data)} news articles')

        # Create Publications
        self.stdout.write('Creating publications...')
        for pub_data in publications_data:
            Publication.objects.get_or_create(
                id=pub_data['id'],
                defaults=pub_data
            )
        self.stdout.write(f'Created {len(publications_data)} publications')

        # Create Events
        self.stdout.write('Creating events...')
        for event_data in events_data:
            Event.objects.get_or_create(
                id=event_data['id'],
                defaults=event_data
            )
        self.stdout.write(f'Created {len(events_data)} events')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with existing data!')
        )
