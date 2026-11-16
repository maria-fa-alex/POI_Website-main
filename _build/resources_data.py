"""Session Resources: one entry per session, newest last.

To add a session: put its PDFs in docs/slides/, add an entry at the bottom of
SESSIONS, then run  python _build/build.py  from the website folder.

  slides     - POI-branded slide deck (PROTECTED: viewer only, watermark, no download)
  guide      - motion walkthrough / notes (UNRESTRICTED: can be read, printed, downloaded)
  guide_name - short name shown in the viewer title, e.g. "Phones in Schools"
  description can contain simple HTML (<em>, &mdash;, &ldquo; &rdquo; ...).
"""

SESSIONS = [
    dict(
        num=1,
        date="Sunday 20th September 2026",
        title="Intro to BP Debate",
        description=("An introduction to the British Parliamentary debate format &mdash; roles, structure, speaking order, motion types, and planning strategy."),
        slides="Intro_to_BP_Debate_Session_1.pdf",
        guide=None,
        guide_name=None,
    ),
    dict(
        num=2,
        date="Sunday 27th September 2026",
        title="Simple Mechanisms",
        description=("Definitions, structured rebuttals, Points of Information (POIs), building robust chains of analysis, and speech signposting &mdash; includes full motion walkthrough guide for <em>&ldquo;This House Would ban the use of AI in schools&rdquo;</em>."),
        slides="Simple_Mechanisms_Session_2.pdf",
        guide="Session_2_Motion_Work_Through_AI_in_Schools.pdf",
        guide_name="AI in Schools",
    ),
    dict(
        num=3,
        date="Sunday 4th October 2026",
        title="OG and OO",
        description=("Roles and strategies for the Opening Half &mdash; Prime Minister (PM), Leader of Opposition (LO), Deputy Prime Minister (DPM), and Deputy Leader of Opposition (DLO). Covers defining the motion, world framing, team cases, and rebuttals &mdash; includes full motion walkthrough guide for <em>&ldquo;This House Would not force students to learn a foreign language&rdquo;</em>."),
        slides="OG_and_OO_Session_3.pdf",
        guide="Session_3_Motion_Work_Through_Foreign_Languages.pdf",
        guide_name="Foreign Languages",
    ),
    dict(
        num=4,
        date="Sunday 11th October 2026",
        title="Role of the Members",
        description=("Roles and strategies for the Member speeches in the Closing Half &mdash; Member of Government (MG) and Member of Opposition (MO). Covers framing team cases, introducing extensions to build upon the Opening Half, and all-round rebuttals &mdash; includes full motion walkthrough guide for <em>&ldquo;This House Believes that phones should be banned in schools&rdquo;</em>."),
        slides="Members_Session_4.pdf",
        guide="Session_4_Motion_Work_Through_Phones_in_Schools.pdf",
        guide_name="Phones in Schools",
    ),
    dict(
        num=5,
        date="Sunday 18th October 2026",
        title="Motion Planning &amp; Walkthrough",
        description=("In-depth debate preparation and motion analysis for <em>&ldquo;This House Would abolish prison as a punishment for non-violent crimes&rdquo;</em> &mdash; featuring Government definitions, UK legal context (Magistrates' Courts), recidivism, and prison overcrowding arguments alongside Opposition counter-framing, general deterrence, incapacitation, and the limits of non-custodial penalties."),
        slides=None,
        guide="Session_5_Motion_Work_Through_Prison_for_Non_Violent_Crimes.pdf",
        guide_name="Abolish Prison for Non-Violent Crimes",
    ),
    dict(
        num=6,
        date="Sunday 8th November 2026",
        title="Review of BP",
        description=("A comprehensive review of British Parliamentary debate strategy and motion planning for <em>&ldquo;This House Would abolish the death penalty&rdquo;</em> &mdash; covering Government definitions, the intrinsic right to life, limited state power, fiscal and opportunity costs, and wrongful convictions alongside Opposition rebuttals, public safety, retributive justice, and deterrence."),
        slides=None,
        guide="Session_6_Motion_Work_Through_Death_Penalty.pdf",
        guide_name="Abolish the Death Penalty",
    ),
    dict(
        num=7,
        date="Sunday 15th November 2026",
        title="Whipping",
        description=("Roles and strategies for the final two speakers in the Closing Half &mdash; Government Whip (GW) and Opposition Whip (OW). Covers whip responsibilities (no new points, refuting opposing arguments without undermining your Opening team, rebuilding extensions, and weighing), structuring speeches around Points of Clash, and a worked Proposition whip example &mdash; includes full motion walkthrough guide for <em>&ldquo;This House Would stop granting awards to media that use AI&rdquo;</em>."),
        slides="Whipping_Session_7.pdf",
        guide="Session_7_Motion_Work_Through_Awards_for_AI_Media.pdf",
        guide_name="Awards for AI Media",
    ),
]
