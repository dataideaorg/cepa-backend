from django.core.management.base import BaseCommand
from focusareas.models import (
    FocusArea, FocusAreaBasicInformation, FocusAreaObjective,
    FocusAreaActivity, FocusAreaOutcome, FocusAreaPartner, FocusAreaMilestone
)
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate focus areas from the markdown document'

    def handle(self, *args, **options):
        """Populate all focus areas"""
        focus_areas_data = self.get_focus_areas_data()

        for idx, area_data in enumerate(focus_areas_data, 1):
            self.create_focus_area(area_data, idx)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Successfully created: {area_data["title"]}')
            )

        self.stdout.write(
            self.style.SUCCESS('\n✓ All focus areas have been populated successfully!')
        )

    def create_focus_area(self, data, order):
        """Create a focus area with all related objects"""
        # Create or update FocusArea
        slug = slugify(data['title'])
        focus_area, created = FocusArea.objects.get_or_create(
            slug=slug,
            defaults={'title': data['title']}
        )

        # Create or update BasicInformation
        basic_info, _ = FocusAreaBasicInformation.objects.get_or_create(
            focus_area=focus_area,
            defaults={
                'overview_summary': data['overview'],
                'status': 'Active',
                'start_date': data['start_date'],
                'order': order
            }
        )

        # Create objectives
        for idx, objective in enumerate(data.get('objectives', []), 1):
            FocusAreaObjective.objects.get_or_create(
                focus_area=focus_area,
                text=objective,
                defaults={'order': idx}
            )

        # Create activities
        for idx, activity in enumerate(data.get('activities', []), 1):
            FocusAreaActivity.objects.get_or_create(
                focus_area=focus_area,
                text=activity,
                defaults={'order': idx}
            )

        # Create outcomes
        for idx, outcome in enumerate(data.get('outcomes', []), 1):
            FocusAreaOutcome.objects.get_or_create(
                focus_area=focus_area,
                title=outcome['title'],
                defaults={
                    'description': outcome.get('description', ''),
                    'metric': outcome.get('metric', ''),
                    'order': idx
                }
            )

        # Create partners
        for idx, partner in enumerate(data.get('partners', []), 1):
            FocusAreaPartner.objects.get_or_create(
                focus_area=focus_area,
                name=partner['name'],
                defaults={
                    'type': partner.get('type', 'NGO Partners'),
                    'role': partner.get('role', ''),
                    'order': idx
                }
            )

    def get_focus_areas_data(self):
        """Return all focus areas data"""
        return [
            {
                'title': 'Parliament Watch Uganda',
                'slug': 'parliament-watch-uganda',
                'overview': 'Parliament Watch Uganda (PW) is CEPA\'s flagship parliamentary monitoring initiative, established in 2013 to bridge the gap between Parliament and citizens. It promotes transparency, accountability, and civic engagement by providing real-time legislative analysis, evidence-based advocacy, and digital platforms that make Uganda\'s Parliament open, accessible, and responsive to the people.',
                'start_date': '2013',
                'objectives': [
                    'Enhance parliamentary transparency and citizen access to legislative information',
                    'Strengthen accountability through monitoring and analysis of parliamentary processes',
                    'Build civic engagement platforms for youth and marginalized communities',
                    'Improve media coverage and reporting on parliamentary affairs'
                ],
                'activities': [
                    'Real-time monitoring and live coverage of plenary and committee sessions',
                    'Weekly parliamentary highlights and legislative analysis',
                    'Digital platform development for civic engagement (Budget Tracker, Debt Tracker, PPT)',
                    'Youth Parliament and Youth Debate Championships',
                    'Regional radio civic education programs',
                    'Parliamentary accountability support to committees'
                ],
                'outcomes': [
                    {'title': 'Pioneered Live Digital Coverage', 'description': 'Parliament Watch pioneered live digital coverage of plenary and committee sessions, now adopted by Parliament itself.', 'metric': '100+ Sessions Covered'},
                    {'title': 'Citizen Access Enhanced', 'description': 'Increased citizen access to timely, accurate, and analytical information on legislative processes.', 'metric': '50,000+ Annual Users'},
                    {'title': 'Media Literacy Improved', 'description': 'Improved media literacy and accuracy in parliamentary reporting through partnerships with UPPA.', 'metric': '200+ Trained Journalists'},
                    {'title': 'Youth Voices Amplified', 'description': 'Expanded inclusion of youth voices through the National Youth Parliament and Youth Debate Championships.', 'metric': '2,000+ Youth Participants'},
                    {'title': 'Data-driven Civic Tools', 'description': 'Created data-driven civic tech tools (Budget Tracker, Debt Tracker, PPT) that have become standard references in Ugandan policy advocacy.', 'metric': '3 Digital Tools'}
                ],
                'partners': [
                    {'name': 'National Endowment for Democracy (NED)', 'type': 'Donor', 'role': 'Primary funder for Parliament Watch Uganda since 2014'},
                    {'name': 'Parliament of Uganda', 'type': 'Government', 'role': 'Key institutional partner and data provider'},
                    {'name': 'Uganda Parliamentary Press Association (UPPA)', 'type': 'Media Partners', 'role': 'Media partner for parliamentary coverage'},
                    {'name': 'Faraja Africa Foundation', 'type': 'NGO Partners', 'role': 'Co-convener of Youth Parliament'},
                    {'name': 'Twaweza East Africa', 'type': 'NGO Partners', 'role': 'Evidence and citizen engagement partner'},
                    {'name': 'Westminster Foundation for Democracy (WFD)', 'type': 'Donor', 'role': 'Support for parliamentary strengthening'},
                    {'name': 'Konrad Adenauer Stiftung (KAS)', 'type': 'Donor', 'role': 'Civic tech platform development support'}
                ]
            },
            {
                'title': 'Road Safety Advocacy',
                'slug': 'road-safety-advocacy',
                'overview': 'The Road Safety Advocacy Programme at CEPA promotes safer roads and stronger policies through evidence-based advocacy, research, and legislative engagement. Since 2018, CEPA has advanced reforms targeting the five key behavioral risk factors—speeding, drink driving, seatbelt use, helmet use, and child restraint—while driving major wins in road safety financing and policy reform.',
                'start_date': '2018',
                'objectives': [
                    'Strengthen policy and regulatory frameworks for behavioral risk factor management',
                    'Increase government investment in road safety interventions',
                    'Build multi-stakeholder coalitions for sustained advocacy',
                    'Evidence-based advocacy on road safety financing and budgeting'
                ],
                'activities': [
                    'Technical review workshops on behavioral risk factors',
                    'Policy dialogues with Ministry of Works and Transport and Parliament',
                    'Road Safety Financing advocacy and budget analysis',
                    'ROSACU coordination and coalition building',
                    'National Road Safety Conferences and stakeholder meetings',
                    'Media campaigns on helmet use, speed management, and seatbelts'
                ],
                'outcomes': [
                    {'title': '733% Budget Increase', 'description': 'CEPA successfully influenced a 733.33% increase in the national road safety budget allocation to the Ministry of Works and Transport for FY2023/24—the largest percentage increase in Uganda\'s road safety financing history.', 'metric': '733.33% Increase'},
                    {'title': 'Policy and Regulatory Wins', 'description': 'Supported drafting and validation of the Traffic and Road Safety Regulations (2023) targeting five key behavioral risk factors.', 'metric': '5 Risk Factors Addressed'},
                    {'title': 'Institutional Strengthening', 'description': 'Supported the Ministry of Works and Transport in reviewing the National Road Safety Policy and aligning it with the amended Act (2020) and NRSAP (2023–2030).', 'metric': '3 Policy Documents'},
                    {'title': 'Parliamentary Resolution', 'description': 'Worked with MPs in the Parliamentary Forum on Road Safety to table and pass a Parliamentary Resolution on Road Safety (December 2021).', 'metric': 'Parliament Resolution Passed'},
                    {'title': 'Coalition Building', 'description': 'Co-founded the Road Safety Advocacy Coalition Uganda (ROSACU) to unify advocacy voices across government, civil society, and private sector.', 'metric': '25+ Institutions'}
                ],
                'partners': [
                    {'name': 'Global Road Safety Partnership (GRSP)', 'type': 'International Partner', 'role': 'Primary technical partner and coordinator'},
                    {'name': 'Bloomberg Philanthropies', 'type': 'Donor', 'role': 'Funding for road safety initiatives (BIGRS)'},
                    {'name': 'Ministry of Works and Transport', 'type': 'Government', 'role': 'Government agency partner for policy implementation'},
                    {'name': 'Parliament of Uganda', 'type': 'Government', 'role': 'Legislative partner through Physical Infrastructure Committee'},
                    {'name': 'Global Health Advocacy Incubator (GHAI)', 'type': 'International Partner', 'role': 'Political economy analysis and advocacy support'},
                    {'name': 'Safe Way Right Way', 'type': 'NGO Partners', 'role': 'Coalition member organization'},
                    {'name': 'Hope for Victims of Traffic Accidents (HOVITA)', 'type': 'NGO Partners', 'role': 'Coalition member organization'}
                ]
            },
            {
                'title': 'Health Advocacy',
                'slug': 'health-advocacy',
                'overview': 'CEPA\'s Health Advocacy Programme drives legislative, policy, and public engagement around emerging health priorities in Uganda. Through research and evidence-based advocacy, CEPA supports reforms on health technologies, alcohol regulation, reproductive health rights, and non-communicable diseases (NCDs), ensuring Parliament and policymakers make informed, equitable, and people-centered decisions.',
                'start_date': '2021',
                'objectives': [
                    'Promote evidence-based dialogue on emerging health technologies and their governance',
                    'Strengthen legislative frameworks for alcohol control and public health',
                    'Advance reproductive health rights and gender-inclusive health policies',
                    'Enhance parliamentary engagement with health committees and experts'
                ],
                'activities': [
                    'Health Tech Platform research and stakeholder consultations',
                    'MP inductions and training on health technologies',
                    'Science journalism support through media training',
                    'Alcohol policy research and participation in UAPC',
                    'HART Bill Twitter Spaces and public engagement',
                    'Human Organ Donation law analysis and public education',
                    'Policy research and commentary on health legislation'
                ],
                'outcomes': [
                    {'title': 'Health Tech Platform Established', 'description': 'Created Uganda\'s first evidence-based Health Tech Platform for emerging technologies and public health innovation.', 'metric': '1 Platform Created'},
                    {'title': 'Alcohol Control Debate Advanced', 'description': 'Advanced the Alcohol Control Bill debate, influencing public discourse and legislative direction.', 'metric': '4 Policy Briefs'},
                    {'title': 'HART Bill Engagement', 'description': 'Shaped national understanding of the HART Bill through inclusive civic dialogues.', 'metric': '3 X Spaces'},
                    {'title': 'Organ Donation Law Analysis', 'description': 'Produced widely referenced commentaries on Organ Donation and Transplant Law, influencing ethical and legislative perspectives.', 'metric': '2 Articles Published'},
                    {'title': 'Health-Governance Leadership', 'description': 'Positioned CEPA as a thought leader in the intersection between health policy, governance, and human rights in Uganda.', 'metric': 'Regional Recognition'}
                ],
                'partners': [
                    {'name': 'African Institute for Development Policy (AFIDEP)', 'type': 'Research Partners', 'role': 'Co-implementer of Health Tech Platform'},
                    {'name': 'Bill & Melinda Gates Foundation', 'type': 'Donor', 'role': 'Funder for Health Tech Platform'},
                    {'name': 'Prime Minister\'s Delivery Unit', 'type': 'Government', 'role': 'Institutional collaborator'},
                    {'name': 'Ministry of Health', 'type': 'Government', 'role': 'Policy and implementation partner'},
                    {'name': 'Uganda Alcohol Policy Alliance (UAPA)', 'type': 'NGO Partners', 'role': 'Alcohol regulation advocacy partner'},
                    {'name': 'Makerere School of Public Health', 'type': 'Research Partners', 'role': 'Research and technical support'},
                    {'name': 'Women\'s Probono Initiative (WPI)', 'type': 'NGO Partners', 'role': 'HART Bill advocacy partner'}
                ]
            },
            {
                'title': 'Human Rights and Civic Space',
                'slug': 'human-rights-civic-space',
                'overview': 'The Human Rights and Civic Space Programme at CEPA promotes rights-based governance and defends civic freedoms by advancing accountability, inclusion, and justice. CEPA works with Parliament, the Uganda Human Rights Commission, media, and civil society to strengthen human rights protection mechanisms and ensure an enabling environment for participation and expression.',
                'start_date': '2016',
                'objectives': [
                    'Strengthen Parliament\'s capacity to protect and promote human rights',
                    'Enhance monitoring of civic space and freedom violations',
                    'Build regional networks for human rights protection',
                    'Support media and civil society engagement on rights issues'
                ],
                'activities': [
                    'Annual UHRC Human Rights Report analysis and dissemination',
                    'Parliamentary Human Rights Committee capacity building',
                    'Civic space monitoring and data collection',
                    'Digital rights training and awareness campaigns',
                    'Anti-Homosexuality Law analysis and public engagement',
                    'Roundtable discussions with state duty bearers',
                    'Journalist training and media grants for human rights reporting'
                ],
                'outcomes': [
                    {'title': 'Parliamentary Capacity Strengthened', 'description': 'Strengthened Parliament\'s institutional capacity to engage with human rights frameworks and UHRC reports.', 'metric': '100+ MPs Trained'},
                    {'title': 'Policy Debates Shaped', 'description': 'Contributed to major policy debates, including Uganda\'s Anti-Homosexuality Law (2023) and freedom of expression reforms.', 'metric': '5+ Policy Papers'},
                    {'title': 'Civic Space Monitoring', 'description': 'Developed Uganda\'s first regional civic space monitoring database and digital rights manual.', 'metric': '1 Database Created'},
                    {'title': 'Human Rights Dialogues', 'description': 'Facilitated over 10 high-level human rights dialogues and 20 online podcasts addressing civic space, accountability, and justice.', 'metric': '30+ Engagements'},
                    {'title': 'Media Empowerment', 'description': 'Empowered 40+ journalists and media professionals to report objectively and accurately on rights issues.', 'metric': '40+ Journalists'}
                ],
                'partners': [
                    {'name': 'Avocats Sans Frontières (ASF)', 'type': 'NGO Partners', 'role': 'Civic Space Initiative co-implementer'},
                    {'name': 'Belgian Development Cooperation (DGD)', 'type': 'Donor', 'role': 'Funder for Civic Space Initiative'},
                    {'name': 'Uganda Human Rights Commission (UHRC)', 'type': 'Government', 'role': 'Institutional partner for rights monitoring'},
                    {'name': 'Parliament of Uganda', 'type': 'Government', 'role': 'Human Rights Committee partner'},
                    {'name': 'Diakonia', 'type': 'International Partner', 'role': 'Long-term development partner'},
                    {'name': 'Human Rights Centre Uganda (HRCU)', 'type': 'NGO Partners', 'role': 'Civil society coalition partner'},
                    {'name': 'Africa Centre for Media Excellence (ACME)', 'type': 'Media Partners', 'role': 'Media training and grants partner'}
                ]
            },
            {
                'title': 'Youth Participation & Democratic Governance',
                'slug': 'youth-participation-democratic-governance',
                'overview': 'CEPA\'s Youth Legislative Advocacy Platform empowers young Ugandans to shape public policy. Since 2016, we\'ve convened Regional & National Youth Parliaments, led debates, produced annual State of the Youth Reports, supported the Uganda Parliamentary Forum on Youth Affairs, and built evidence for youth-centered reforms through research, business forums, and the Youth Policy Journal.',
                'start_date': '2016',
                'objectives': [
                    'Empower youth to participate actively in policy advocacy and legislative processes',
                    'Build evidence on youth priorities and development needs',
                    'Strengthen youth-Parliament interface through structured engagement',
                    'Develop youth leadership and governance capacity'
                ],
                'activities': [
                    'Regional and National Youth Parliament convening and facilitation',
                    'Annual Youth Debate Championship organization',
                    'State of the Youth Report production and dissemination',
                    'Uganda Parliamentary Forum on Youth Affairs technical support',
                    'Annual Youth Business Forum for entrepreneurship engagement',
                    'Youth Policy Journal peer review and publication',
                    'Mentorship and Leadership Labs for select cohorts'
                ],
                'outcomes': [
                    {'title': 'Institutionalised Youth Parliaments', 'description': 'Institutionalised Youth Parliaments feeding real motions and recommendations to committees and UPFYA annually.', 'metric': '9+ Years Running'},
                    {'title': 'National Debate Pipeline', 'description': 'National debate pipeline building persuasive, evidence-based youth advocates across universities and regions.', 'metric': '5,000+ Participants'},
                    {'title': 'Evidence-to-Action', 'description': 'State of the Youth Reports informing committee briefings, petitions, and oversight questions.', 'metric': '9+ Annual Reports'},
                    {'title': 'Entrepreneurship Policy', 'description': 'Entrepreneurship policy asks surfaced through the Youth Business Forum (regulatory and financing barriers).', 'metric': '20+ Recommendations'},
                    {'title': 'Parliamentary Linkage', 'description': 'Sustained parliamentary linkage via UPFYA technical support and regular joint engagements.', 'metric': '100+ MPs Engaged'}
                ],
                'partners': [
                    {'name': 'Faraja Africa Foundation', 'type': 'NGO Partners', 'role': 'National Youth Parliament co-convener'},
                    {'name': 'Debate Society Uganda', 'type': 'NGO Partners', 'role': 'Youth Debate Championship partner'},
                    {'name': 'Parliament of Uganda', 'type': 'Government', 'role': 'UPFYA host and institutional partner'},
                    {'name': 'French Embassy/Equipe France Fund', 'type': 'International Partner', 'role': 'Youth leadership initiatives funder'},
                    {'name': 'Konrad-Adenauer-Stiftung (KAS)', 'type': 'Donor', 'role': 'Civic tech support for youth engagement'},
                    {'name': 'Lead Impact Hub', 'type': 'Private Sector', 'role': 'Entrepreneurship ecosystem partner'},
                    {'name': 'Twaweza East Africa', 'type': 'NGO Partners', 'role': 'Evidence and citizen engagement partner'}
                ]
            },
            {
                'title': 'Transparency & Accountability',
                'slug': 'transparency-accountability',
                'overview': 'CEPA\'s Transparency and Accountability programme strengthens fiscal oversight, anti-corruption mechanisms, and public engagement in governance. Through sustained research, policy advocacy, and collaboration with accountability committees, CEPA advances open budget processes, audit responsiveness, and evidence-based dialogue on integrity, financial management, and service delivery at both national and local government levels.',
                'start_date': '2014',
                'objectives': [
                    'Strengthen parliamentary oversight of fiscal management and budget execution',
                    'Enhance public understanding and engagement in accountability processes',
                    'Support institutional responsiveness to audit findings and recommendations',
                    'Build evidence on corruption trends and institutional reform needs'
                ],
                'activities': [
                    'Analysis and dissemination of Auditor General Annual Reports',
                    'Budget transparency and public finance analysis',
                    'IGG Corruption Report analysis and commentary',
                    'Parliamentary accountability committee technical support',
                    'Citizens\' Guide to accountability reports production',
                    'Public Sector Integrity Dialogues facilitation',
                    'Local government accountability forums in select districts'
                ],
                'outcomes': [
                    {'title': 'Committee Strengthening', 'description': 'Strengthened cooperation between CEPA and Parliament\'s accountability committees, enabling timely and informed review of audit reports.', 'metric': '50+ Briefs Provided'},
                    {'title': 'Public Access Enhanced', 'description': 'Public access to audit and budget information through CEPA\'s publications and digital platforms.', 'metric': '10,000+ Annual Readers'},
                    {'title': 'Evidence-Based Oversight', 'description': 'Evidence-based oversight: over 50 analytical briefs submitted to committees since 2017.', 'metric': '50+ Briefs'},
                    {'title': 'Public Discourse', 'description': 'Contributed to public discourse on corruption, institutional redundancy, and fiscal discipline.', 'metric': '100+ Media Pieces'},
                    {'title': 'Media Amplification', 'description': 'Media amplification through partnerships with UPPA, expanding citizens\' understanding of accountability processes.', 'metric': '50+ Stories'}
                ],
                'partners': [
                    {'name': 'Office of the Auditor General', 'type': 'Government', 'role': 'Audit report data source and partner'},
                    {'name': 'Inspectorate of Government (IGG)', 'type': 'Government', 'role': 'Corruption report partner and collaborator'},
                    {'name': 'Ministry of Finance, Planning and Economic Development', 'type': 'Government', 'role': 'Budget policy and data partner'},
                    {'name': 'Parliament of Uganda', 'type': 'Government', 'role': 'Accountability committees partner'},
                    {'name': 'Twaweza East Africa', 'type': 'NGO Partners', 'role': 'Evidence and citizen engagement partner'},
                    {'name': 'Global Integrity', 'type': 'International Partner', 'role': 'Anti-corruption partner'},
                    {'name': 'Friedrich Ebert Stiftung (FES)', 'type': 'Donor', 'role': 'Accountability and governance support'}
                ]
            },
            {
                'title': 'Climate Justice & Environmental Governance',
                'slug': 'climate-justice-environmental-governance',
                'overview': 'CEPA\'s Climate Justice and Environmental Governance programme promotes people-centred climate action through evidence-based advocacy, parliamentary engagement, and community mobilisation. We advance equitable policies on climate change, environment, and extractives by supporting Parliament\'s oversight, empowering citizens, and bridging science, policy, and community resilience initiatives across Uganda\'s regions.',
                'start_date': '2019',
                'objectives': [
                    'Strengthen parliamentary leadership and accountability on climate policy',
                    'Advance community-centered climate action and environmental restoration',
                    'Research and advocate on extractives, oil, and climate intersectionality',
                    'Support integration of climate finance tracking in budget processes'
                ],
                'activities': [
                    'Parliamentary Climate Governance Initiative support and research',
                    'Community climate action and tree-planting programme implementation',
                    'Extractives and climate governance research and policy briefs',
                    'Climate policy and budget analysis series production',
                    'Local climate resilience forums in Gulu, Mbale, and Soroti',
                    'Parliamentary Climate Conversations and expert dialogues',
                    'Community sensitization on sustainable agriculture and waste management'
                ],
                'outcomes': [
                    {'title': 'Parliamentary Oversight Strengthened', 'description': 'Strengthened Parliamentary oversight on climate governance, with CEPA recognized as a technical partner to the Climate Committee and Forum.', 'metric': '5+ Policy Briefs'},
                    {'title': 'Public Participation Enhanced', 'description': 'Enhanced public participation in environmental decision-making through community dialogues and reforestation drives.', 'metric': '15,000+ Trees Planted'},
                    {'title': 'Extractives Research', 'description': 'Conducted pioneering research on oil, extractives, and climate intersectionality, shaping public debate on sustainable energy transitions.', 'metric': '3 Research Papers'},
                    {'title': 'Climate Finance Tracking', 'description': 'Supported integration of climate finance tracking within Parliament\'s budget analysis processes.', 'metric': '3+ Years Tracking'},
                    {'title': 'Gender and Climate Justice', 'description': 'Raised awareness of gender and climate justice, particularly the role of women in adaptation and environmental stewardship.', 'metric': '2 Gender Reports'}
                ],
                'partners': [
                    {'name': 'Diakonia Uganda', 'type': 'International Partner', 'role': 'Community climate action program co-implementer'},
                    {'name': 'Friedrich Ebert Stiftung (FES)', 'type': 'Donor', 'role': 'Climate governance research support'},
                    {'name': 'Global Green Growth Institute (GGGI)', 'type': 'International Partner', 'role': 'Climate policy partner'},
                    {'name': 'African Institute for Development Policy (AFIDEP)', 'type': 'Research Partners', 'role': 'Climate research collaboration'},
                    {'name': 'Parliament of Uganda', 'type': 'Government', 'role': 'Climate Committee and Forum partner'},
                    {'name': 'Ministry of Water and Environment', 'type': 'Government', 'role': 'Environmental policy partner'},
                    {'name': 'Makerere University', 'type': 'Research Partners', 'role': 'Climate research and capacity building'}
                ]
            },
            {
                'title': 'Artificial Intelligence, Digital Governance & Innovation',
                'slug': 'ai-digital-governance-innovation',
                'overview': 'CEPA\'s Artificial Intelligence and Digital Governance Programme champions responsible, inclusive, and rights-based technology in policymaking. Through research, civic tech innovation, and multi-stakeholder engagement, CEPA works to ensure emerging technologies like AI advance democracy, transparency, and equitable development while safeguarding human rights and digital inclusion across Africa.',
                'start_date': '2023',
                'objectives': [
                    'Promote ethical and inclusive AI governance frameworks in African legislatures',
                    'Develop digital tools for enhanced parliamentary transparency and citizen engagement',
                    'Research and advocate on AI\'s role in policy-making and democratic governance',
                    'Support youth and civil society in understanding and engaging with digital innovation'
                ],
                'activities': [
                    'Africa Artificial Intelligence Summit (AAIS) convening and facilitation',
                    'AI in Governance and Legislative Innovation Initiative implementation',
                    'Digital Parliament and Civic Tech Tools development (Budget, Debt, PPT Trackers)',
                    'AI and Youth Civic Engagement pilot programs',
                    'Research on AI and Policy in Africa',
                    'AI and Democracy Conversations podcast and dialogue series',
                    'AI Training Manual for Parliament development and rollout'
                ],
                'outcomes': [
                    {'title': 'Africa AI Summit Co-Convened', 'description': 'Co-convened Africa\'s first continental AI Summit, advancing policy consensus on ethical, inclusive AI.', 'metric': '300+ Participants'},
                    {'title': 'AI Mainstreamed in Governance', 'description': 'Mainstreamed AI in Uganda\'s governance discourse, linking innovation with legislative reform.', 'metric': '5+ Policy Papers'},
                    {'title': 'AI Governance Frameworks', 'description': 'Developed AI governance frameworks and tools to guide Parliament and policymakers.', 'metric': '1 Manual + Toolkit'},
                    {'title': 'AI-Integrated Civic Tech', 'description': 'Created AI-integrated civic tech platforms (Budget Tracker, Debt Tracker, Performance Tracker) for evidence-based oversight.', 'metric': '3 Digital Tools'},
                    {'title': 'Regional Thought Leader', 'description': 'Positioned CEPA as a regional thought leader in AI governance, ethics, and legislative transformation.', 'metric': 'Continental Recognition'}
                ],
                'partners': [
                    {'name': 'Ministry of ICT & National Guidance', 'type': 'Government', 'role': 'AI strategy and digital transformation partner'},
                    {'name': 'Uganda Communications Commission (UCC)', 'type': 'Government', 'role': 'Regulatory partner for digital governance'},
                    {'name': 'Centre for Entrepreneurship and Executive Development (CEED)', 'type': 'Private Sector', 'role': 'Africa AI Summit co-convener'},
                    {'name': 'PopVox Foundation', 'type': 'International Partner', 'role': 'Digital governance technology partner'},
                    {'name': 'Makerere University AI Research Lab', 'type': 'Research Partners', 'role': 'AI research and capacity building'},
                    {'name': 'Global Partnership on Artificial Intelligence (GPAI)', 'type': 'International Partner', 'role': 'Global AI governance network'},
                    {'name': 'Friedrich Ebert Stiftung (FES)', 'type': 'Donor', 'role': 'AI ethics and policy research support'}
                ]
            }
        ]
