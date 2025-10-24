from django.core.management.base import BaseCommand
from focusareas.models import (
    FocusArea, FocusAreaObjective, FocusAreaActivity,
    FocusAreaOutcome, FocusAreaPartner, FocusAreaMilestone
)


class Command(BaseCommand):
    help = 'Populate focus areas with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate focus areas...')

        # Clear existing data
        self.stdout.write('Clearing existing focus areas...')
        FocusArea.objects.all().delete()

        focus_areas_data = [
            {
                'slug': 'parliament-watch',
                'title': 'Parliament Watch',
                'description': 'Monitoring parliamentary proceedings and ensuring accountability in legislative processes.',
                'image': '/focus-areas/parliament.jpg',
                'overview_summary': "Our Parliament Watch program is dedicated to promoting transparency, accountability, and citizen engagement in Uganda's legislative process. We monitor parliamentary sessions, analyze voting patterns, and provide detailed reports on legislative activities.",
                'status': 'Active',
                'start_date': 'January 2020',
                'order': 1,
                'objectives': [
                    'Enhance transparency in parliamentary proceedings',
                    'Promote accountability among members of parliament',
                    'Increase citizen awareness and participation in legislative processes',
                    'Strengthen oversight mechanisms'
                ],
                'activities': [
                    'Real-time monitoring of parliamentary sessions',
                    'Analysis of voting patterns and attendance',
                    'Committee oversight and reporting',
                    'Legislative impact assessments'
                ],
                'outcomes': [
                    {
                        'title': 'Increased Parliamentary Transparency',
                        'description': 'Published over 50 detailed reports on parliamentary proceedings, reaching 100,000+ citizens',
                        'metric': '50+ Reports'
                    },
                    {
                        'title': 'Enhanced Public Engagement',
                        'description': 'Facilitated dialogue between citizens and MPs through town halls and online platforms',
                        'metric': '20+ Town Halls'
                    },
                    {
                        'title': 'Policy Influence',
                        'description': 'Our research has informed 15+ policy reforms and legislative amendments',
                        'metric': '15+ Reforms'
                    }
                ],
                'partners': [
                    {
                        'name': 'Parliament of Uganda',
                        'type': 'Government',
                        'role': 'Data sharing and collaboration on transparency initiatives'
                    },
                    {
                        'name': 'Democratic Governance Facility',
                        'type': 'Donor',
                        'role': 'Financial support and capacity building'
                    },
                    {
                        'name': 'Civil Society Organizations',
                        'type': 'NGO Partners',
                        'role': 'Joint advocacy and grassroots mobilization'
                    }
                ],
                'milestones': [
                    {'year': '2020', 'event': 'Program launch and initial monitoring framework'},
                    {'year': '2021', 'event': 'Expanded coverage to all parliamentary committees'},
                    {'year': '2022', 'event': 'Launched digital platform for citizen engagement'},
                    {'year': '2023', 'event': 'Introduced AI-powered analysis tools'},
                    {'year': '2024', 'event': 'Partnership expansion and regional impact'}
                ]
            },
            {
                'slug': 'democracy',
                'title': 'Parliamentary Democracy and Governance',
                'description': 'Strengthening democratic institutions and promoting good governance practices.',
                'image': '/focus-areas/democracy.jpg',
                'overview_summary': "We work to enhance democratic processes, improve institutional capacity, and promote participatory governance at all levels of government. Our approach combines research, advocacy, and capacity building to strengthen Uganda's democratic foundations.",
                'status': 'Active',
                'start_date': 'March 2019',
                'order': 2,
                'objectives': [
                    'Strengthen democratic institutions and processes',
                    'Promote inclusive and participatory governance',
                    'Enhance electoral integrity',
                    'Build capacity of democratic actors'
                ],
                'activities': [
                    'Democratic institution strengthening',
                    'Electoral process monitoring',
                    'Governance capacity building',
                    'Citizen participation enhancement'
                ],
                'outcomes': [
                    {
                        'title': 'Institutional Capacity Building',
                        'description': 'Trained 500+ government officials and civil society leaders on democratic governance',
                        'metric': '500+ Trained'
                    },
                    {
                        'title': 'Electoral Reforms',
                        'description': 'Contributed to electoral law reforms through evidence-based advocacy',
                        'metric': '5 Key Reforms'
                    },
                    {
                        'title': 'Civic Participation',
                        'description': 'Increased citizen participation in governance processes by 40%',
                        'metric': '+40% Engagement'
                    }
                ],
                'partners': [
                    {
                        'name': 'Electoral Commission',
                        'type': 'Government',
                        'role': 'Electoral process monitoring and capacity building'
                    },
                    {
                        'name': 'International IDEA',
                        'type': 'International Partner',
                        'role': 'Technical support and knowledge sharing'
                    },
                    {
                        'name': 'Local Government Networks',
                        'type': 'Government',
                        'role': 'Implementation of governance initiatives'
                    }
                ],
                'milestones': [
                    {'year': '2019', 'event': 'Program establishment and baseline research'},
                    {'year': '2020', 'event': 'First cohort of governance training programs'},
                    {'year': '2021', 'event': 'Electoral process monitoring during general elections'},
                    {'year': '2022', 'event': 'Policy advocacy for governance reforms'},
                    {'year': '2024', 'event': 'Scaling impact to regional level'}
                ]
            },
            {
                'slug': 'transparency',
                'title': 'Transparency and Accountability',
                'description': 'Advocating for open government and holding leaders accountable to citizens.',
                'image': '/focus-areas/transparency.jpg',
                'overview_summary': 'We promote transparency in government operations, advocate for access to information, and work to ensure public officials are held accountable for their actions. Our work focuses on public expenditure tracking, anti-corruption initiatives, and government transparency monitoring.',
                'status': 'Active',
                'start_date': 'July 2018',
                'order': 3,
                'objectives': [
                    'Promote transparency in government operations',
                    'Strengthen access to information frameworks',
                    'Combat corruption through evidence-based advocacy',
                    'Enhance accountability mechanisms'
                ],
                'activities': [
                    'Access to information advocacy',
                    'Public expenditure tracking',
                    'Anti-corruption initiatives',
                    'Government transparency monitoring'
                ],
                'outcomes': [
                    {
                        'title': 'Budget Transparency',
                        'description': 'Successfully tracked UGX 500B+ in public expenditure, identifying efficiency gaps',
                        'metric': 'UGX 500B+ Tracked'
                    },
                    {
                        'title': 'Information Access',
                        'description': 'Supported 200+ citizens in accessing government information through legal aid',
                        'metric': '200+ Cases'
                    },
                    {
                        'title': 'Anti-Corruption Impact',
                        'description': 'Our reports led to investigations of 10+ corruption cases',
                        'metric': '10+ Investigations'
                    }
                ],
                'partners': [
                    {
                        'name': 'Transparency International',
                        'type': 'International Partner',
                        'role': 'Technical support and global advocacy coordination'
                    },
                    {
                        'name': "Auditor General's Office",
                        'type': 'Government',
                        'role': 'Data collaboration and joint accountability initiatives'
                    },
                    {
                        'name': 'Media Houses',
                        'type': 'Media Partners',
                        'role': 'Dissemination of research findings'
                    }
                ],
                'milestones': [
                    {'year': '2018', 'event': 'Transparency program launch'},
                    {'year': '2019', 'event': 'First public expenditure tracking report'},
                    {'year': '2020', 'event': 'Access to information legal aid clinic established'},
                    {'year': '2022', 'event': 'Launch of digital transparency platform'},
                    {'year': '2024', 'event': 'Expanded anti-corruption monitoring'}
                ]
            },
            {
                'slug': 'human-rights',
                'title': 'Human Rights',
                'description': 'Protecting and promoting fundamental human rights and freedoms.',
                'image': '/focus-areas/human-rights.jpg',
                'overview_summary': 'We monitor human rights violations, advocate for policy reforms, and work to ensure that all Ugandans can enjoy their fundamental rights and freedoms. Our approach combines documentation, legal support, and policy advocacy.',
                'status': 'Active',
                'start_date': 'September 2017',
                'order': 4,
                'objectives': [
                    'Monitor and document human rights violations',
                    'Provide legal aid and support to victims',
                    'Advocate for human rights policy reforms',
                    'Raise awareness on human rights issues'
                ],
                'activities': [
                    'Human rights monitoring and reporting',
                    'Policy advocacy for rights protection',
                    'Legal aid and support services',
                    'Rights awareness campaigns'
                ],
                'outcomes': [
                    {
                        'title': 'Rights Documentation',
                        'description': 'Documented and reported 100+ human rights violations to relevant authorities',
                        'metric': '100+ Cases'
                    },
                    {
                        'title': 'Legal Support',
                        'description': 'Provided legal aid to 150+ individuals facing rights violations',
                        'metric': '150+ Supported'
                    },
                    {
                        'title': 'Policy Impact',
                        'description': 'Contributed to 8 human rights policy reforms at national level',
                        'metric': '8 Reforms'
                    }
                ],
                'partners': [
                    {
                        'name': 'Uganda Human Rights Commission',
                        'type': 'Government',
                        'role': 'Joint monitoring and advocacy initiatives'
                    },
                    {
                        'name': 'International Human Rights Organizations',
                        'type': 'International Partner',
                        'role': 'Capacity building and resource support'
                    },
                    {
                        'name': 'Legal Aid Service Providers',
                        'type': 'NGO Partners',
                        'role': 'Legal support and representation'
                    }
                ],
                'milestones': [
                    {'year': '2017', 'event': 'Human rights program established'},
                    {'year': '2018', 'event': 'First comprehensive rights monitoring report'},
                    {'year': '2020', 'event': 'Legal aid clinic opened'},
                    {'year': '2022', 'event': 'Digital rights monitoring system launched'},
                    {'year': '2024', 'event': 'Expanded coverage to marginalized communities'}
                ]
            },
            {
                'slug': 'health',
                'title': 'Public Health and Road Safety',
                'description': 'Improving public health outcomes and road safety across Uganda.',
                'image': '/focus-areas/health.jpg',
                'overview_summary': 'We conduct research on public health issues, advocate for better healthcare policies, and work to improve road safety through evidence-based interventions. Our focus is on policy research, advocacy, and community awareness.',
                'status': 'Active',
                'start_date': 'May 2019',
                'order': 5,
                'objectives': [
                    'Improve public health policy and implementation',
                    'Reduce road traffic accidents and fatalities',
                    'Enhance healthcare system accountability',
                    'Promote health awareness and education'
                ],
                'activities': [
                    'Public health policy research',
                    'Healthcare system analysis',
                    'Road safety advocacy',
                    'Health awareness campaigns'
                ],
                'outcomes': [
                    {
                        'title': 'Policy Influence',
                        'description': 'Our research informed 10+ health policy reforms at national and district levels',
                        'metric': '10+ Reforms'
                    },
                    {
                        'title': 'Road Safety Impact',
                        'description': 'Advocacy contributed to 25% reduction in road accidents in targeted districts',
                        'metric': '-25% Accidents'
                    },
                    {
                        'title': 'Community Reach',
                        'description': 'Health awareness campaigns reached 200,000+ individuals',
                        'metric': '200K+ Reached'
                    }
                ],
                'partners': [
                    {
                        'name': 'Ministry of Health',
                        'type': 'Government',
                        'role': 'Policy collaboration and data sharing'
                    },
                    {
                        'name': 'WHO Country Office',
                        'type': 'International Partner',
                        'role': 'Technical support and capacity building'
                    },
                    {
                        'name': 'Traffic Police',
                        'type': 'Government',
                        'role': 'Road safety initiatives and enforcement'
                    }
                ],
                'milestones': [
                    {'year': '2019', 'event': 'Health and road safety program launch'},
                    {'year': '2020', 'event': 'COVID-19 policy response research'},
                    {'year': '2021', 'event': 'Road safety campaign in 5 districts'},
                    {'year': '2023', 'event': 'Healthcare accountability framework developed'},
                    {'year': '2024', 'event': 'Scaling health initiatives nationally'}
                ]
            },
            {
                'slug': 'climate',
                'title': 'Climate Justice',
                'description': 'Addressing climate change impacts and promoting environmental sustainability.',
                'image': '/focus-areas/climate.jpg',
                'overview_summary': 'We research climate change impacts on Uganda, advocate for sustainable policies, and work with communities to build resilience against climate-related challenges. Our approach integrates research, advocacy, and community action.',
                'status': 'Active',
                'start_date': 'January 2020',
                'order': 6,
                'objectives': [
                    'Document climate change impacts on communities',
                    'Advocate for climate-responsive policies',
                    'Build community resilience to climate change',
                    'Promote sustainable development practices'
                ],
                'activities': [
                    'Climate impact assessments',
                    'Environmental policy advocacy',
                    'Community resilience building',
                    'Sustainable development promotion'
                ],
                'outcomes': [
                    {
                        'title': 'Research Impact',
                        'description': 'Published 20+ research reports on climate impacts informing national policy',
                        'metric': '20+ Reports'
                    },
                    {
                        'title': 'Community Resilience',
                        'description': 'Built climate resilience in 50+ communities through adaptation programs',
                        'metric': '50+ Communities'
                    },
                    {
                        'title': 'Policy Advocacy',
                        'description': 'Contributed to 6 climate-related policy reforms',
                        'metric': '6 Reforms'
                    }
                ],
                'partners': [
                    {
                        'name': 'Ministry of Water and Environment',
                        'type': 'Government',
                        'role': 'Policy collaboration and implementation'
                    },
                    {
                        'name': 'Climate Action Network',
                        'type': 'NGO Partners',
                        'role': 'Joint advocacy and knowledge sharing'
                    },
                    {
                        'name': 'International Climate Funds',
                        'type': 'Donor',
                        'role': 'Financial support for climate programs'
                    }
                ],
                'milestones': [
                    {'year': '2020', 'event': 'Climate justice program established'},
                    {'year': '2021', 'event': 'First climate vulnerability assessment'},
                    {'year': '2022', 'event': 'Community resilience programs launched'},
                    {'year': '2023', 'event': 'Climate policy advocacy campaigns'},
                    {'year': '2024', 'event': 'Scaling climate action initiatives'}
                ]
            },
            {
                'slug': 'ai',
                'title': 'Artificial Intelligence (AI)',
                'description': 'Leveraging technology and AI for better governance and policy outcomes.',
                'image': '/focus-areas/artificial-intelligence.jpg',
                'overview_summary': 'We explore how AI and technology can improve governance, enhance service delivery, and support evidence-based policy making in Uganda. Our work focuses on AI policy research, digital rights advocacy, and innovation in public services.',
                'status': 'Active',
                'start_date': 'October 2021',
                'order': 7,
                'objectives': [
                    'Research AI policy frameworks for Uganda',
                    'Advocate for ethical AI governance',
                    'Promote digital rights and data protection',
                    'Support innovation in public service delivery'
                ],
                'activities': [
                    'AI policy research and analysis',
                    'Technology governance frameworks',
                    'Digital rights advocacy',
                    'Innovation in public service delivery'
                ],
                'outcomes': [
                    {
                        'title': 'Policy Development',
                        'description': 'Contributed to draft AI governance framework for Uganda',
                        'metric': '1 Framework'
                    },
                    {
                        'title': 'Capacity Building',
                        'description': 'Trained 100+ government officials on AI and digital governance',
                        'metric': '100+ Trained'
                    },
                    {
                        'title': 'Innovation Support',
                        'description': 'Supported 15+ government AI pilot projects',
                        'metric': '15+ Projects'
                    }
                ],
                'partners': [
                    {
                        'name': 'Ministry of ICT',
                        'type': 'Government',
                        'role': 'Policy development and implementation'
                    },
                    {
                        'name': 'Tech Companies',
                        'type': 'Private Sector',
                        'role': 'Technical expertise and innovation support'
                    },
                    {
                        'name': 'Academic Institutions',
                        'type': 'Research Partners',
                        'role': 'Joint research and capacity building'
                    }
                ],
                'milestones': [
                    {'year': '2021', 'event': 'AI governance program launched'},
                    {'year': '2022', 'event': 'First AI policy research report published'},
                    {'year': '2023', 'event': 'Digital rights advocacy campaign'},
                    {'year': '2024', 'event': 'AI governance framework development'}
                ]
            },
            {
                'slug': 'scrutiny',
                'title': 'Post Legislative Scrutiny',
                'description': 'Assessing the effectiveness of laws and policies after implementation.',
                'image': '/focus-areas/democracy.jpg',
                'overview_summary': 'We conduct systematic reviews of implemented policies and laws to assess their effectiveness, identify gaps, and recommend improvements for better outcomes. Our approach combines rigorous evaluation with stakeholder engagement.',
                'status': 'Active',
                'start_date': 'June 2020',
                'order': 8,
                'objectives': [
                    'Evaluate effectiveness of implemented legislation',
                    'Identify implementation gaps and challenges',
                    'Recommend evidence-based improvements',
                    'Promote learning and policy adaptation'
                ],
                'activities': [
                    'Policy effectiveness evaluations',
                    'Legislative impact assessments',
                    'Implementation monitoring',
                    'Policy improvement recommendations'
                ],
                'outcomes': [
                    {
                        'title': 'Policy Evaluations',
                        'description': 'Completed 25+ comprehensive post-legislative scrutiny reviews',
                        'metric': '25+ Reviews'
                    },
                    {
                        'title': 'Policy Improvements',
                        'description': 'Recommendations led to amendments of 12 laws and policies',
                        'metric': '12 Amendments'
                    },
                    {
                        'title': 'Stakeholder Engagement',
                        'description': 'Engaged 500+ stakeholders in scrutiny processes',
                        'metric': '500+ Engaged'
                    }
                ],
                'partners': [
                    {
                        'name': 'Parliament of Uganda',
                        'type': 'Government',
                        'role': 'Collaboration on legislative review processes'
                    },
                    {
                        'name': 'Policy Research Institutes',
                        'type': 'Research Partners',
                        'role': 'Joint evaluation studies'
                    },
                    {
                        'name': 'Line Ministries',
                        'type': 'Government',
                        'role': 'Implementation data and stakeholder engagement'
                    }
                ],
                'milestones': [
                    {'year': '2020', 'event': 'Post-legislative scrutiny program launched'},
                    {'year': '2021', 'event': 'First batch of policy evaluations completed'},
                    {'year': '2022', 'event': 'Scrutiny framework adopted by Parliament'},
                    {'year': '2023', 'event': 'Expanded scope to include regulatory reviews'},
                    {'year': '2024', 'event': 'Digital monitoring systems implemented'}
                ]
            }
        ]

        # Create focus areas with related data
        for area_data in focus_areas_data:
            self.stdout.write(f"Creating focus area: {area_data['title']}")

            # Create focus area
            focus_area = FocusArea.objects.create(
                slug=area_data['slug'],
                title=area_data['title'],
                description=area_data['description'],
                image=area_data['image'],
                overview_summary=area_data['overview_summary'],
                status=area_data['status'],
                start_date=area_data['start_date'],
                order=area_data['order']
            )

            # Create objectives
            for idx, objective_text in enumerate(area_data['objectives']):
                FocusAreaObjective.objects.create(
                    focus_area=focus_area,
                    text=objective_text,
                    order=idx
                )

            # Create activities
            for idx, activity_text in enumerate(area_data['activities']):
                FocusAreaActivity.objects.create(
                    focus_area=focus_area,
                    text=activity_text,
                    order=idx
                )

            # Create outcomes
            for idx, outcome_data in enumerate(area_data['outcomes']):
                FocusAreaOutcome.objects.create(
                    focus_area=focus_area,
                    title=outcome_data['title'],
                    description=outcome_data['description'],
                    metric=outcome_data['metric'],
                    order=idx
                )

            # Create partners
            for idx, partner_data in enumerate(area_data['partners']):
                FocusAreaPartner.objects.create(
                    focus_area=focus_area,
                    name=partner_data['name'],
                    type=partner_data['type'],
                    role=partner_data['role'],
                    order=idx
                )

            # Create milestones
            for idx, milestone_data in enumerate(area_data['milestones']):
                FocusAreaMilestone.objects.create(
                    focus_area=focus_area,
                    year=milestone_data['year'],
                    event=milestone_data['event'],
                    order=idx
                )

            self.stdout.write(self.style.SUCCESS(f"✓ Created {area_data['title']}"))

        self.stdout.write(self.style.SUCCESS(f'\n Successfully populated {len(focus_areas_data)} focus areas!'))
