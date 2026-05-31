from __future__ import annotations

import html
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
OLD_HOST = "www.munyachipunza.com"
OLD_IP = "185.230.63.171"
SITE_URL = "https://munyachipunza.com"
SITE_DESCRIPTION = "Personal essays by Munya Chipunza on faith, resilience, fatherhood, grief, leadership, and finding hope in hard seasons."
BLOG_APP_ID = "14bcded7-0066-7c35-14d7-466cb3f09103"
POSTS_PER_PAGE = 5
ASSET_VERSION = "20260531b"
CONTENT_POSTS_DIR = ROOT / "content" / "posts"
AUDIO_DIR = ROOT / "assets" / "audio"
GOOGLE_ANALYTICS_TAG = """    <script async src="https://www.googletagmanager.com/gtag/js?id=G-4J3RHW9XRZ"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-4J3RHW9XRZ');
    </script>"""
ICON_LINKS = """    <link rel="icon" href="/favicon.ico" sizes="any">
    <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">"""
SUBSCRIBE_MODE = "buttondown"  # Use "holding" while Buttondown account review is pending.
CONTACT_FORM_PROVIDER = "web3forms"
CONTACT_FORM_ACTION = "https://api.web3forms.com/submit"
CONTACT_FORM_AJAX = "https://api.web3forms.com/submit"
WEB3FORMS_ACCESS_KEY = "f9d1b737-cd21-4a16-abce-4c950aea6379"
CONTACT_EMAIL = "hello@munyachipunza.com"
CONTACT_SUCCESS_URL = f"{SITE_URL}/thanks"
BUTTONDOWN_USERNAME = "munyachipunza"
BUTTONDOWN_SUBSCRIBE_ACTION = f"https://buttondown.com/api/emails/embed-subscribe/{BUTTONDOWN_USERNAME}"

POST_CONFIG = {
    "the-weight-of-unspoken-words": {
        "route": "weight-of-unspoken-words",
        "tag": "Faith & Resilience",
    },
    "self-worth-how-much-do-you-value-yourself": {
        "route": "self-worth",
        "tag": "Identity",
    },
    "peace-can-be-safe-too": {
        "route": "peace-can-be-safe",
        "tag": "Peace",
    },
    "sometimes-it-s-ok-to-be-not-ok": {
        "route": "not-ok",
        "tag": "Resilience",
    },
    "when-all-seems-to-be-going-wrong": {
        "route": "when-all-goes-wrong",
        "tag": "Faith",
    },
    "when-the-enemy-is-the-inner-me": {
        "route": "enemy-inner-me",
        "tag": "Identity",
    },
    "the-power-of-thank-you": {
        "route": "the-power-of-thank-you",
        "tag": "Gratitude",
    },
    "words-that-build-not-break": {
        "route": "words-that-build-not-break",
        "tag": "Communication",
    },
    "from-burden-to-blessing-shifting-the-lens-of-leadership-and-life": {
        "route": "shifting-the-lens-of-leadership-and-life",
        "tag": "Leadership",
    },
    "when-the-leader-runs-empty": {
        "route": "when-the-leader-runs-empty",
        "tag": "Leadership",
    },
    "pressure-reveals-the-leader": {
        "route": "pressure-reveals-the-leader",
        "tag": "Leadership",
    },
    "dare-to-lead": {
        "route": "dare-to-lead",
        "tag": "Leadership",
    },
}

LOCAL_POSTS = [
    {
        "old_slug": "a-letter-to-the-younger-me-and-you",
        "route": "a-letter-to-the-younger-me-and-you",
        "tag": "Birthday Reflection",
        "title": "A Letter to the Younger Me and You",
        "summary": "A birthday reflection on turning 33, being formed in hard seasons, and learning that the life you are building is not behind schedule.",
        "excerpt": "A birthday reflection on turning 33, being formed in hard seasons, and learning that the life you are building is not behind schedule.",
        "published_date": "2026-05-14T12:00:00Z",
        "updated_date": "2026-05-14T12:00:00Z",
        "minutes_to_read": 5,
        "paragraphs": [
            "As I turn 33 today, I find myself thinking about the version of me that did not know we would make it here.",
            "You are reading this from inside a season that feels like it has no exit.",
            "I know. I was there.",
            "You are carrying things that have no name yet. Pressure that does not announce itself but sits in your chest from the moment you open your eyes. Relationships that cost more than they should. A version of yourself you are trying to become while the current version is barely keeping up. Money that is never quite enough. Dreams that feel embarrassingly large for someone in your situation.",
            "You are wondering if you are behind.",
            "You are not behind. You are being formed.",
            "I need you to understand something about the season you are in. It is not a waiting room. It is not a punishment. It is not evidence that God forgot your address or that the life you imagined was naive.",
            "It is the making of you.",
            "Not the comfortable version of you. Not the version that arrived easily and therefore carries nothing. The version that will one day sit with someone who is where you are right now - and will know exactly what to say because you lived this. Because you did not leave early. Because you stayed in the fire long enough to stop being afraid of heat.",
            "That version is who you are becoming.",
            "But I want to be honest with you about some things nobody told me.",
            "The comparison will cost you more than the struggle. The struggle is hard but it is honest. The comparison is a thief. It will take ordinary days and turn them into evidence of failure. It will take other people's highlight reels and hold them against your behind-the-scenes. Stop. Your story is not running on their timeline. It never was.",
            "The people who love you are not your audience. You do not need to perform recovery for the people closest to you. You do not need to appear further along than you are. Let them see the real version. The one that is tired and trying and still showing up. That version is more loveable than you think. And the relationships where you can be that version - hold onto those with both hands.",
            "Faith is not the absence of doubt. It is movement in the presence of it. You will have seasons where God feels far and the silence is deafening and the prayers feel like they are hitting the ceiling. Pray anyway. Show up anyway. The faith that survives that season is worth more than the faith that never had to.",
            "You will not always get credit for what you carry. Some of your best work will be invisible. Some of your hardest seasons will be ones nobody sees. The meeting nobody knew almost broke you. The night nobody witnessed when you chose right. The quiet decision to stay when leaving would have been easier. God saw it. It counted. It is being written into something larger than you can see right now.",
            "And this - the most important thing.",
            "The life you are building is not behind schedule.",
            "Thirty three is not late. It is not the beginning of the end of your chances. It is not the point where the window closes and the options narrow. Some of the most important chapters of your life have not started yet. Some of the people who will matter most to you have not arrived yet. Some of the work that will carry your name has not been written yet.",
            "You are not behind.",
            "You are exactly where the making requires you to be.",
            "Keep going. Not because it is easy. Not because it is clear. Not because you can see how it resolves.",
            "Keep going because the person you are becoming needs you to.",
            "And one day - not as far from now as it feels - you will sit somewhere quiet and realise that everything you went through was doing something. That none of it was wasted. That the hard seasons were not detours from the story.",
            "They were the story.",
            "You made it to here.",
            "That is not nothing.",
            "That is everything.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "being-needed-does-not-mean-being-unlimited",
        "route": "being-needed-does-not-mean-being-unlimited",
        "tag": "Boundaries",
        "title": "Being Needed Does Not Mean Being Unlimited",
        "summary": "A reflection on love, limits, and the truth that being needed does not mean becoming endless for everyone else.",
        "excerpt": "A reflection on love, limits, and the truth that being needed does not mean becoming endless for everyone else. You can be a place of comfort without disappearing.",
        "published_date": "2026-05-13T12:00:00Z",
        "updated_date": "2026-05-13T12:00:00Z",
        "minutes_to_read": 5,
        "paragraphs": [
            "There is a certain tiredness that comes when one more person needs something from you.",
            "Not because you do not love them. That is the difficult part. You do love them. You care about the call, the message, the child, the parent, the friend, the work, the home, the person who is asking. You understand why they need you. You may even understand why they came to you first.",
            "But something in you also knows there is not much left to give.",
            "That is where the guilt begins. Because when you are someone people rely on, needing space can feel like betrayal. Rest can feel selfish. Silence can feel rude. Saying, \"I cannot today,\" can feel like you are failing someone who trusted you enough to ask.",
            "So you stretch. You take the call when you wanted quiet. You reply when you had nothing left in you. You help with one more thing. You listen a little longer. You make a plan because people expect you to make a plan. You become useful again, even when what you needed most was to stop being useful for a while.",
            "At first, it can look like love.",
            "And sometimes it is. Love does show up. Love does carry. Love does make room for another person's need. Love does inconvenience itself. Love does stay when it would be easier to walk away.",
            "But there is a kind of carrying that slowly stops being love and starts becoming disappearance.",
            "You are there for everyone, but less present in yourself. You become reliable, but tired. Helpful, but quietly resentful. Available, but slowly empty. The difficult part is that people may not notice. Not because they are cruel, but because they have become used to you being the one who can handle it.",
            "The one who will understand. The one who will answer. The one who will come through. The one who will not complain. The one who somehow always finds capacity.",
            "And maybe you have trained them to believe that.",
            "Not intentionally. Just by always finding a way.",
            "This can happen anywhere. In a family. In a friendship. In a marriage. In a classroom. In a workplace. In a home where the list never ends. In a season of grief where people still expect you to function. In a quiet life where everyone assumes that because you have time, you must also have capacity.",
            "Being needed is not the problem. It can be a gift. It means your presence matters somewhere. It means someone feels steadier because you exist. It means your life carries weight in another person's world.",
            "That is not small.",
            "But being needed does not mean being unlimited.",
            "You are not wrong for having edges. You are not selfish because you cannot carry everything today. You are not unloving because your heart, body, mind, or spirit needs room to breathe.",
            "The hard part is learning that not every need is your assignment. Some needs are yours to carry. Some are yours to share. Some are yours to help with for a season. And some were never yours, even if they arrived with urgency and your name attached to them.",
            "That is difficult when people are used to your yes. The first time you tell the truth about your limits, it can feel like you are doing something wrong. You can feel guilty for not replying. Cruel for resting. Weak for admitting that you are tired too.",
            "But maybe some things were never meant to be held by one person alone.",
            "Maybe the problem is not that you are failing to carry enough. Maybe the problem is that you have been carrying what was meant to be shared.",
            "There is a difference between loving people and becoming endless for them. There is a difference between helping and disappearing. There is a difference between being present and teaching everyone that you do not need care too.",
            "I think a lot of resentment starts there.",
            "Not because we stopped loving people, but because we kept saying yes after the honest answer had become, \"I am tired too\".",
            "When love is forced to keep moving without truth, it begins to change shape. It still helps, but with less warmth. It still shows up, but with hidden anger. It still says yes, but somewhere inside, it starts keeping score.",
            "That is usually a sign that something has been ignored for too long.",
            "Maybe the healthier love is not the one that has no limits. Maybe it is the one honest enough to remain alive. The kind that can say, \"I care, but I cannot today\". The kind that can say, \"I want to help, but I need a moment\". The kind that can say, \"I am here, but I cannot be everything\".",
            "That does not make the love smaller.",
            "It may make it cleaner.",
            "Because the people who truly need you do not only need what you can do. They need you still whole enough to be present. Still soft enough to love well. Still honest enough to say when the weight is becoming too much.",
            "You are allowed to be needed and still be human. You are allowed to love people deeply without becoming an endless supply.",
            "Maybe that is not selfish.",
            "Maybe that is how love stays alive.",
            "Being needed is meaningful.",
            "But being needed does not mean being unlimited.",
            "You can be a place of comfort without disappearing inside everyone else's need.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "the-version-you-did-not-become",
        "route": "the-version-you-did-not-become",
        "tag": "Healing",
        "title": "The Version You Did Not Become",
        "summary": "A reflection on the quiet mercy of not becoming the sharpest version of yourself when hurt shows up first.",
        "excerpt": "A reflection on the quiet mercy of not becoming the sharpest version of yourself when hurt shows up first. Sometimes love is what you refuse to release.",
        "published_date": "2026-05-12T12:00:00Z",
        "updated_date": "2026-05-12T12:00:00Z",
        "minutes_to_read": 4,
        "paragraphs": [
            "There are moments when something touches the sore place in you.",
            "Not always something big.",
            "A message.",
            "A look.",
            "A correction.",
            "A joke that went too far.",
            "A question asked at the wrong time.",
            "The feeling of being ignored.",
            "The quiet ache of not being understood.",
            "And suddenly, another version of you starts looking for a way out.",
            "The sharper one.",
            "The colder one.",
            "The one that wants to answer pain with pain.",
            "Sometimes it comes through words.",
            "Sometimes through silence.",
            "Sometimes through distance.",
            "Sometimes through a face that says everything your mouth is trying not to say.",
            "It is strange how quickly hurt can look for somewhere to go.",
            "One moment, you are just feeling something.",
            "The next, your tone has changed. Your patience has thinned. Your kindness has stepped back. And someone in front of you is now about to meet a version of you that was shaped by a wound they may not even know they touched.",
            "I have been thinking about those moments.",
            "Not the big failures everyone can see.",
            "The small ones before they happen.",
            "The sentence you almost said.",
            "The message you almost sent.",
            "The look you almost gave.",
            "The silence you almost used as punishment.",
            "The pride you almost protected.",
            "There is a quiet kind of mercy in not becoming the worst thing you felt.",
            "No one claps for that.",
            "No one knows how close you were. No one sees the words you deleted. No one sees the breath you took before answering differently. No one sees the part of you that wanted to harden, but did not get to lead.",
            "But maybe some of the most important victories in a life are like that.",
            "Unseen.",
            "Not dramatic.",
            "Just a person choosing not to pass their pain forward.",
            "Because sometimes love is not what you say.",
            "Sometimes love is what you refuse to release.",
            "The anger that stops with you.",
            "The irritation that does not get inherited.",
            "The heaviness that does not become someone else's wound.",
            "That matters.",
            "Especially in a world where everyone is carrying something, and everyone has a reason to be sharp.",
            "Maybe comfort is not always soft words.",
            "Maybe sometimes comfort is restraint.",
            "Maybe sometimes hope is given by the person who had every reason to become hard, but chose not to.",
            "Today, I am grateful for the version of me that did not get to lead.",
            "The one that almost spoke.",
            "Almost reacted.",
            "Almost punished.",
            "Almost made someone else carry what was mine to deal with.",
            "And I am learning that becoming better is not always about becoming impressive.",
            "Sometimes it is simply about becoming safer to be around.",
            "A person whose pain does not automatically become another person's burden.",
            "A person who can feel deeply, but still choose gently.",
            "A person who pauses long enough for love to have a say.",
            "That too is a kind of healing.",
            "Not loud.",
            "But real.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "the-love-that-still-speaks",
        "route": "the-love-that-still-speaks",
        "tag": "Family",
        "title": "The Love That Still Speaks",
        "summary": "A Mother's Day reflection. Some love does not disappear when the person is gone. It keeps forming you long after the voice has fallen silent.",
        "excerpt": "A Mother's Day reflection. Some love does not disappear when the person is gone. It keeps forming you long after the voice has fallen silent.",
        "published_date": "2026-05-10T08:00:00Z",
        "updated_date": "2026-05-10T08:00:00Z",
        "minutes_to_read": 3,
        "paragraphs": [
            "I understand Mother's Day differently now.",
            "Not only as a day for flowers, messages, and public honour, but as a day that asks you to look again at what motherhood carried before you were old enough to recognise it.",
            "There are some lives that keep speaking after the person is gone.",
            "Not loudly.",
            "Not every day in obvious ways.",
            "But in the quiet places.",
            "In the way you carry responsibility.",
            "In the way you love your own family.",
            "In the way certain memories return when life asks more from you than you thought you had.",
            "A mother's life can do that.",
            "When you are young, you mostly receive motherhood. You receive the food, the care, the correction, the protection, the prayers, the presence. You know what it feels like to be loved, but you do not always understand what that love was costing.",
            "You do not see all the fears she had to carry quietly.",
            "You do not see how often she had to be strong when she may have wanted to be held herself.",
            "You do not understand that some of what looked normal was actually sacrifice repeated so often that it became part of the furniture of your life.",
            "Then you grow older.",
            "You begin to carry people. You make decisions that affect a household. You worry about things you cannot fully control. You pray differently. You love with more weight in your hands.",
            "And slowly, you start to see your mother with older eyes.",
            "Not just as the one who raised you, but as a person who carried. A person who endured. A person who gave from places that were not always full. A person who had to keep choosing love even when life did not make it easy.",
            "That is why a mother's love can teach you something about God before you even have the language for it.",
            "Not because it is perfect.",
            "But because real love carries.",
            "It covers.",
            "It corrects.",
            "It stays.",
            "It gives.",
            "It protects.",
            "It prays in hidden places.",
            "It keeps showing up long before anyone understands the cost.",
            "Today I honour my mother with a gratitude that has grown deeper with time.",
            "For the sacrifices I saw.",
            "For the sacrifices I did not see.",
            "For the prayers I knew about.",
            "For the prayers I may never know about.",
            "For the strength that shaped me.",
            "For the love that still has fingerprints on who I am becoming.",
            "Mother's Day carries both gratitude and ache.",
            "Gratitude for the gift.",
            "Ache because the gift is no longer held the same way.",
            "But love does not disappear simply because presence changes.",
            "Some love remains in the bones of a family.",
            "Some love keeps forming you long after the voice is gone.",
            "Some love becomes part of how you stand, how you endure, how you believe, and how you love others.",
            "So today, I thank God for her life.",
            "For the mother she was.",
            "For what she carried.",
            "For what she gave.",
            "For what she planted.",
            "For what still remains.",
            "Her presence is missed.",
            "But her love is not gone.",
            "It still speaks.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "the-ceiling-youre-carrying",
        "route": "the-ceiling-youre-carrying",
        "tag": "Resilience",
        "title": "The Ceiling You're Carrying",
        "summary": "A reflection for the bone-tired seasons when you are holding up a ceiling nobody else can see, and staying is enough for today.",
        "excerpt": "A reflection for the bone-tired seasons when you are holding up a ceiling nobody else can see. You are allowed to be tired, and staying is enough for today.",
        "published_date": "2026-05-09T12:00:00Z",
        "updated_date": "2026-05-09T12:00:00Z",
        "minutes_to_read": 2,
        "paragraphs": [
            "There is a kind of tired that sleep does not fix.",
            "Not the tired that comes from a long day or a hard week. The other kind. The kind that sits in your bones and makes even the small things feel heavy. Where you wake up already behind. Where good news and bad news arrive in the same breath and you cannot hold either properly because your hands are already too full.",
            "Like you have been holding up a ceiling that nobody else can see.",
            "And you are not even sure anymore if the ceiling is real — or if you have just been standing in that position for so long you forgot you could put your arms down.",
            "I know that place. You might be familiar with it too. Or maybe you are in it right now — crashing out quietly, holding it together on the outside while something in you is coming apart.",
            "The vision is still there. The thing you are building, the future you can see clearly on a good day — it has not gone anywhere. But today the wanting itself is exhausting. The energy to reach for it is not there. And you cannot explain that to anyone who is not living it because from the outside everything looks fine. You are still showing up. You are still holding it together.",
            "Nobody can see the ceiling.",
            "And then there is the weight of the people who need you. You love them. You genuinely do. And also, sometimes, in the same breath, you feel the weight of it. And before that thought even finishes you already feel guilty for having it.",
            "That is not weakness. That is what it costs to actually care.",
            "I want to tell you something today. I hope it sticks.",
            "You are allowed to be tired. Deeply, honestly, without-a-solution tired. You do not have to locate the lesson in it yet. You do not have to perform recovery for anyone watching.",
            "Sometimes the most faithful thing you can do is stay. Not thrive. Not produce. Not figure it out.",
            "Just stay.",
            "God is not waiting for you to get your energy back before He is present with you. He is here. In this. In the ceiling-holding, bone-tired, crashing-out version of you.",
            "That version is not less. It is not failing.",
            "It is human.",
            "And it is enough for today.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "the-people-who-stay",
        "route": "the-people-who-stay",
        "tag": "Friendship",
        "title": "The People Who Stay",
        "summary": "A reflection on rare friendship, costly loyalty, and the people God sends so we do not carry hard seasons alone.",
        "excerpt": "A reflection on rare friendship, costly loyalty, and the people God sends so we do not carry hard seasons alone. The people who stay when it costs something are rare.",
        "published_date": "2026-05-08T12:00:00Z",
        "updated_date": "2026-05-08T12:00:00Z",
        "minutes_to_read": 3,
        "paragraphs": [
            "There is a kind of friendship that only reveals itself in the hard seasons.",
            "Not the friendship of convenience. Not the kind that shows up when things are easy and the room is full of good news. The kind that walks toward you when everyone else is quietly walking away.",
            "I have been thinking about those people this week.",
            "The ones who did not wait to be asked. Who showed up in the middle of something they had no obligation to enter. Who rearranged their lives, quietly and without ceremony, because they had decided a long time ago that you were worth showing up for.",
            "I think about Jonathan.",
            "In a season where loyalty to David could have cost him everything - his position, his father's favour, his own claim to a future - Jonathan stayed. He warned David of danger. He covered for him. He made a covenant not because it was strategic but because something deep in him had decided: this person matters.",
            "The Bible says Jonathan loved David as his own soul.",
            "That is not a feeling. That is a decision.",
            "I think about Ruth.",
            "When Naomi told her daughters-in-law to go back to their own people, Orpah left. Reasonably. Understandably. It made sense to go. But Ruth stayed. And what she said to Naomi has outlasted both of them: where you go I will go. Where you die I will die.",
            "Ruth did not stay because the situation looked promising. She stayed because the relationship was worth more than the circumstances.",
            "I think about Paul and Silas, side by side in a prison at midnight. No plan. No exit strategy. Just two people who had decided to go through it together. And they sang.",
            "Some of us are in seasons where we need people like that.",
            "Not people with answers. Not people who can fix the thing that is broken. Just people who will sit in the midnight with you and not make it feel like you are alone in it.",
            "If you have even one person like that - a friend who drives across a city, a spouse who keeps showing up, a sibling who calls when it gets quiet, someone who played a role they had no obligation to play just because you needed it - do not take that lightly.",
            "That person is not an accident in your life.",
            "They are a gift from a God who knows exactly how heavy the seasons get, and who has always believed you should not carry them alone.",
            "Tend those relationships. Honour them. Show up for those people the way they show up for you.",
            "Because the world will always have rooms full of people who know your name.",
            "But the people who stay when it costs something - those are rare.",
            "And they are worth everything.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "the-day-you-did-everything-right",
        "route": "the-day-you-did-everything-right",
        "tag": "Faith",
        "title": "The Day You Did Everything Right",
        "summary": "A reflection for the days when you gave your best, the result did not come, and the quiet question rose: was any of it worth it?",
        "excerpt": "A reflection for the days when you gave your best, the result did not come, and the quiet question rose: was any of it worth it? You were seen today.",
        "published_date": "2026-05-07T12:00:00Z",
        "updated_date": "2026-05-07T12:00:00Z",
        "minutes_to_read": 3,
        "paragraphs": [
            "Some days you do everything right.",
            "And it still doesn't work out.",
            "You gave what you had. You showed up when it cost you something. You chose the harder, better thing - and the result you needed did not come. The door stayed closed. The person didn't respond. The situation didn't shift. The morning looked exactly like the one before it.",
            "And somewhere in the quiet, a question rises.",
            "Was any of it worth it?",
            "I have sat with that question. I think most of us have, if we are honest.",
            "There is a kind of tired that has nothing to do with sleep. It is the tired that comes from giving your best and finding the world unmoved. From doing right when wrong would have been easier, and receiving nothing for it. From holding on, quietly, faithfully, while no one is watching and nothing is changing.",
            "That tired is real. And it deserves to be named.",
            "But I have come to believe something about those days.",
            "There is a woman in the Bible who had been suffering for twelve years. She had tried everything available to her. Nothing worked. Everything she had was gone. By every measure, her situation was unchanged.",
            "And then she stopped waiting for the right circumstance to rescue her.",
            "She pushed through a crowd and reached.",
            "Not loudly. Not with a speech or a demand. Just a reach. A quiet, desperate, faithful reach toward the only one she believed could actually help her.",
            "And everything changed.",
            "Not because she finally earned it.",
            "Because she finally reached in the right direction.",
            "Some seasons are not asking you to do more.",
            "They are asking you to reach differently. To stop measuring your worth by what the day returned to you. To remember that the most important witness to your life is not the one who did not notice, did not respond, did not show up.",
            "You were seen today.",
            "In the reaching. In the showing up. In the quiet faithfulness that nobody applauded and nobody counted.",
            "Every bit of it was seen.",
            "And the one who saw it - the one who has always seen it - has never once looked at your life and found it lacking. Not on the hard days. Not on the empty ones. Not on the days you drove home in silence wondering if you were enough.",
            "You were enough then. You are enough now.",
            "Rest in that.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "what-they-see-first",
        "route": "what-they-see-first",
        "tag": "Identity",
        "title": "What They See First",
        "summary": "A reflection on being judged by the surface, and the steady comfort of being seen by God more truthfully than people ever do.",
        "excerpt": "A reflection on being judged by the surface, and the steady comfort of being seen by God more truthfully than people ever do. What people see first is rarely what God sees at all.",
        "published_date": "2026-05-06T12:00:00Z",
        "updated_date": "2026-05-06T12:00:00Z",
        "minutes_to_read": 3,
        "paragraphs": [
            "There are people who will form their opinion before the story is finished.",
            "They will look at what is immediately visible - the obvious difficulty, the thing that makes you move differently - and they will decide there. Before the numbers. Before the output. Before they have stayed long enough to understand what they are actually looking at.",
            "I watched someone be reduced to their surface today.",
            "And it did something to me. Not just frustration. Something older than that. A kind of grief that comes from witnessing a person be unseen when their life is quietly telling a different story.",
            "I kept thinking about David.",
            "When Samuel came to Jesse's house to anoint the next king of Israel, the sons lined up. Tall. Strong. Impressive. The kind of men you look at and immediately believe. And Samuel nearly got it wrong. He looked at what was standing in front of him and thought, this must be the one.",
            "But God said: I do not see as man sees. Man looks at the outward appearance. I look at the heart.",
            "David was still in the fields. Nobody had even thought to call him in.",
            "The one God had already chosen was the one nobody considered worth presenting.",
            "I wonder if you have ever been that person. Left in the field. Not called into the room. Measured by what is immediately visible before anyone asked what you are actually made of.",
            "The quiet output that nobody is tracking. The resilience that does not announce itself. The work happening beneath the surface that the loudest voice in the room has not noticed yet.",
            "It does not mean you are invisible.",
            "It means you are being seen by a different set of eyes.",
            "The ones that matter most have always looked past the surface. They looked at a shepherd boy and saw a king. They looked at a widow with almost nothing and called it abundance. They looked at a man in chains and wrote letters that are still changing lives.",
            "Your story is not finished.",
            "What people see first is rarely what God sees at all.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "the-currency-youre-not-spending",
        "route": "the-currency-youre-not-spending",
        "tag": "Love",
        "title": "The Currency You're Not Spending",
        "summary": "A reflection on love as the one currency that never runs out, and the cost of withholding it when pride wants to stay right.",
        "excerpt": "A reflection on love as the one currency that never runs out, and the cost of withholding it when pride wants to stay right. The wallet will be full again tomorrow.",
        "published_date": "2026-05-11T12:00:00Z",
        "updated_date": "2026-05-11T12:00:00Z",
        "minutes_to_read": 4,
        "paragraphs": [
            "Everyone is walking around with a bottomless wallet.",
            "Not money. Not influence. Not time - though we treat those like they're in short supply too. Something older than all of those. Something that does not deplete no matter how much you give away.",
            "Love.",
            "And most of us are hoarding it.",
            "Not because we don't have it. We have more than we could ever spend. But somewhere along the way we started treating it like a limited resource. Like if we give too much of it to the wrong person, or at the wrong time, or without guarantee of return - we'll run out.",
            "You won't run out.",
            "The wallet refills. It has always refilled. Every morning you wake up, you have exactly as much love to give as you did the day before.",
            "So why do we withhold it?",
            "The honest answer is not that we don't have it. It's that we're protecting something. Pride, mostly. The need to be right. The need to win the argument, hold the position, make the point. The need to make someone feel the weight of what they did before we soften toward them.",
            "We choose to be right instead of choosing to love.",
            "And we tell ourselves it's justified. That the other person needs to earn it back first. That we'll open up again once they've shown they deserve it. But what actually happens is that we stay closed. Days pass. Then weeks. And the hardness that started as a choice quietly becomes a posture. A way of moving through rooms. A way of looking at people.",
            "And everyone in those rooms can feel it.",
            "But here is the thing I want you to sit with.",
            "Think about the people who changed your life.",
            "Not the ones who showed up when it was easy. Not the ones who loved you after you had proven yourself, cleaned yourself up, become someone worth investing in. The ones who changed your life.",
            "Every single one of them loved you before you deserved it.",
            "There is a face coming to mind right now. You know there is. Someone who saw something in you before you saw it in yourself. Someone who stayed when leaving would have been easier. Someone who gave you something - time, words, presence, a chance - and asked for nothing in return. Someone who had every reason to withhold and chose not to.",
            "And because of that person, something in you survived that might not have.",
            "You are still here, in part, because someone spent what was in their wallet on you.",
            "That is not a small thing.",
            "That is the whole argument.",
            "Because here is what that means. It means love works. Not as a theory. Not as a nice idea for people who have the luxury of being soft. As a force. As something that actually changes the outcome. As something that reaches people when nothing else can - when logic fails, when pressure fails, when time has run out.",
            "You are living proof that it works.",
            "And somewhere right now, there is a person waiting for you to be that for them. Maybe you know them. Maybe you see them every day and the hardness between you has become so familiar you've stopped questioning it. Maybe they are someone you haven't met yet, someone whose path will cross yours at exactly the moment they need what you're carrying.",
            "They don't need you to be right.",
            "They need you to spend what's in your wallet.",
            "The receiver can always decline. That is their right. But that is their choice to make - not yours to preempt. Your job is not to decide in advance whether the love will land. Your job is to give it and let it go.",
            "Some of it will be wasted. Some of it will be misread. Some of it will go to people who don't know what to do with it yet.",
            "Give it anyway.",
            "Because the cost of withholding is always higher than the cost of giving. You don't just rob the other person when you choose hardness. You rob yourself. You become a little more closed, a little more defended, a little more certain that the world doesn't deserve what you're carrying.",
            "It does.",
            "You know it does. Because someone once thought the same thing - and then they looked at you and spent it anyway.",
            "Do the same.",
            "The wallet will be full again tomorrow.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    {
        "old_slug": "blank-page-was-still-there",
        "route": "blank-page-was-still-there",
        "tag": "Resilience",
        "title": "The Blank Page Was Still There",
        "summary": "A quiet return after a season of silence, and a reminder that some pauses are survival, not failure.",
        "excerpt": "A quiet return after a season of silence, and a reminder that some pauses are survival, not failure. The blank page does not hold your absence against you. It just opens.",
        "published_date": "2026-05-05T12:00:00Z",
        "updated_date": "2026-05-05T12:00:00Z",
        "minutes_to_read": 2,
        "paragraphs": [
            "I didn't plan to disappear.",
            "That's the thing about going quiet — it rarely starts with a decision. It starts with one week being harder than usual. Then that week becomes two. And somewhere in the middle of it, writing stops feeling like something you do and starts feeling like something you owe people. A debt you're not ready to pay.",
            "So you stay silent. And the longer the silence, the heavier the return feels.",
            "I've been away from this page for a while. Not because I ran out of things to say — if anything, the opposite. Life handed me more than I knew how to write about. Some seasons are like that. They're too full, too raw, too close to the bone to turn into words while you're still inside them.",
            "But here's what I came back to find: the blank page was still there. Waiting. Not accusing. Just waiting.",
            "There's a version of this story I used to believe — that if you stop, you forfeit something. That consistency is the price of being taken seriously. That the gap in your timeline is proof of something. Weakness, maybe. Or lack of discipline.",
            "I don't believe that anymore.",
            "I think some pauses are not failures. They're survival. They're you doing what needed to be done — holding things together, showing up where it mattered most, getting through the part of life that doesn't pause just because you need it to.",
            "The writing will still be here when you come back.",
            "I don't know who needs to hear this today. Maybe you stopped writing. Or praying. Or going to the gym. Or calling the people who matter. Maybe you put something down weeks ago — something that used to give you life — because the weight of everything else was too much.",
            "I want to tell you: the return doesn't have to be an event. You don't need to announce it. You don't need to explain the gap. You don't need to come back louder or more polished to make up for the time away.",
            "You just need to start again. Quietly, if that's all you have.",
            "One sentence. One prayer. One kilometre. One message.",
            "The blank page doesn't hold the absence against you. It just opens.",
            "I'm back. And whatever you put down — whenever you're ready — so are you.",
        ],
        "image_url": f"{SITE_URL}/assets/images/munya-home.jpg",
    },
    # Legacy posts migrated from the old Wix blog. Each entry was extracted
    # from the rendered writing/<route>.html + blog-feed.xml, so the generator
    # no longer needs to call the Wix API. Tags and old slugs preserve the
    # POST_CONFIG mapping so the legacy /post/<old-slug>/ redirects keep working.
    {
        'old_slug': 'the-weight-of-unspoken-words',
        'route': 'weight-of-unspoken-words',
        'tag': 'Faith & Resilience',
        'title': 'The Weight of Unspoken Words',
        'excerpt': "There are things you've been carrying that no one knows about. Words you swallowed instead of spoke. Truths you buried because the timing never felt right. Feelings you tucked away because you didn't want to be a burden. And now, somewhere deep inside, those unspoken words have become a quiet weight — pressing against your chest, sitting in your throat, waiting. We convince ourselves that silence is strength. That holding it in is the mature thing to do. That if we just keep moving, keep...",
        'published_date': '2026-02-05T11:04:55.547Z',
        'updated_date': '2026-02-05T11:04:55.547Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            "There are things you've been carrying that no one knows about.",
            "Words you swallowed instead of spoke. Truths you buried because the timing never felt right. Feelings you tucked away because you didn't want to be a burden. And now, somewhere deep inside, those unspoken words have become a quiet weight — pressing against your chest, sitting in your throat, waiting.",
            "We convince ourselves that silence is strength. That holding it in is the mature thing to do. That if we just keep moving, keep smiling, keep showing up — eventually, the weight will lift on its own. But it doesn't. It settles. It grows heavier with time.",
            'The conversation you never had with your father or mother. The apology you owed but pride wouldn\'t let you give. The "I love you" you assumed they already knew. The boundary you needed to set but feared would cost you the relationship. The cry for help that stayed trapped behind "I\'m fine. "',
            'Unspoken words don\'t disappear. They live in the tension of relationships that never quite feel whole. They echo in the distance between you and someone you once felt close to. They show up as resentment, regret, or the quiet ache of "what if I had just said something? "',
            "Sometimes we stay silent to protect others. But often, if we're honest, we stay silent to protect ourselves — from rejection, from conflict, from being seen as too much or not enough. And so we carry it. Alone.",
            "But here's the truth: your words matter. Your feelings deserve to be heard — not just by others, but by yourself. Speaking doesn't always mean confrontation. Sometimes it's simply letting yourself be known. Sometimes it's writing it down. Sometimes it's finally admitting to God what you've been too afraid to say out loud.",
            "You don't have to carry everything in silence. You weren't designed to. The things left unsaid have a way of shaping us — but so do the things we finally release.",
            'Maybe today is the day you put down some of that weight. Maybe it starts with one honest conversation. One vulnerable moment. One step toward the freedom that comes when you stop holding it all in.',
            "Your voice has value. Your truth has a place. And the words you've been carrying? They're ready to be set free.",
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_239fb7de1ac74bb3b2b2d84070a6609e~mv2.jpg',
    },
    {
        'old_slug': 'self-worth-how-much-do-you-value-yourself',
        'route': 'self-worth',
        'tag': 'Identity',
        'title': 'Self-Worth: How much do you value yourself?',
        'excerpt': 'There are days when you look in the mirror and can’t quite meet your own eyes. Not because you’re vain, but because you’ve forgotten who you are. Somewhere between the noise of expectations, disappointments, and silent comparisons, your reflection became blurred. You start to measure yourself by what didn’t work out, by who walked away, by what you still haven’t achieved. And slowly, your sense of worth becomes something you have to earn instead of something you already have. That’s what the...',
        'published_date': '2025-11-05T08:33:08.490Z',
        'updated_date': '2025-11-05T08:33:08.490Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'There are days when you look in the mirror and can’t quite meet your own eyes. Not because you’re vain, but because you’ve forgotten who you are. Somewhere between the noise of expectations, disappointments, and silent comparisons, your reflection became blurred.',
            'You start to measure yourself by what didn’t work out, by who walked away, by what you still haven’t achieved. And slowly, your sense of worth becomes something you have to earn instead of something you already have.',
            'That’s what the world does to us — it teaches us that worth must be proven. If you do enough, give enough, achieve enough, maybe you’ll finally be enough. But deep down, we all know the truth: the harder we chase validation, the more fragile it becomes. Because anything that isn’t rooted in God’s truth can be taken away.',
            'You see, self-worth isn’t found in the applause, the title, or even in being loved by the right people. Those things are fleeting. Your worth was sealed long before you made your first mistake, long before your heart was broken, long before life taught you how to hide your pain behind productivity.',
            'You are worthy because God said so. You are valuable because He breathed His image into you. And nothing—no failure, no heartbreak, no rejection—can erase that divine fingerprint.',
            'Still, it’s not easy to believe this when the world keeps shouting otherwise. We all have moments when the silence feels heavy, when our prayers seem to bounce back unanswered, when life feels like a series of almosts and not-enoughs. In those moments, the enemy doesn’t always come with loud accusations. Sometimes, he whispers in the voice of your own doubt: <em>You’re falling behind. You’re not doing enough. You’re not worth much.</em> And because it sounds familiar, you start to believe it.',
            'But God doesn’t measure you the way the world does. He’s not waiting for your perfection — He’s waiting for your surrender. When you come to Him empty, tired, and unsure of yourself, He doesn’t turn away. He restores. He reminds you that the cracks in your confidence are not flaws to be hidden, but places where His light enters. He whispers softly, <em>You are still mine. You have always been mine.</em>',
            'So when you forget your worth, return to the One who gave it to you. When the lies grow louder, sit in His Word until you can hear truth again. When your heart tells you that you’re not enough, remember that you never had to be — because grace already covered that gap.',
            'You are not your failures. You are not your labels. You are not the person the world misjudged or the version of yourself that fear created. You are chosen, seen, and deeply loved — even in your uncertainty.',
            'And maybe, that’s where healing begins — not in striving to become more, but in resting in the truth that you already are.',
            'Because the Creator of heaven and earth looked at you and said, <em>It is good.</em>',
            'And that… will always be enough.',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_56e355244df849f4a598a4443538d355~mv2.png',
    },
    {
        'old_slug': 'peace-can-be-safe-too',
        'route': 'peace-can-be-safe',
        'tag': 'Peace',
        'title': 'Peace Can Be Safe, Too',
        'excerpt': 'Sometimes, the calm feels suspicious. You finally get a moment of quiet — no fires to put out, no problems demanding your attention — and instead of peace, you feel panic. Your mind starts searching for what’s about to go wrong. You brace for impact that never comes. It’s strange, isn’t it? Strange how even in calm waters, we find ourselves waiting for the next storm. That’s because peace doesn’t always feel safe when you’ve lived through chaos. Your body remembers. It remembers the nights...',
        'published_date': '2025-10-30T08:50:51.371Z',
        'updated_date': '2025-10-30T08:50:51.371Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'Sometimes, the calm feels suspicious. You finally get a moment of quiet — no fires to put out, no problems demanding your attention — and instead of peace, you feel panic. Your mind starts searching for what’s about to go wrong. You brace for impact that never comes.',
            'It’s strange, isn’t it?',
            'Strange how even in calm waters, we find ourselves waiting for the next storm.',
            'That’s because peace doesn’t always feel safe when you’ve lived through chaos. Your body remembers. It remembers the nights you couldn’t sleep because everything was falling apart. It remembers the seasons when comfort didn’t last and joy was always temporary. So when life finally gives you a breath, your mind whispers — <em>“Don’t trust it. Something bad must be coming.”</em>',
            'But here’s the truth. You’re not broken. You’re just healing.',
            'Your body is still learning that it doesn’t have to stay in survival mode. That rest isn’t danger. That love doesn’t always disappear. That calm isn’t the setup for pain.',
            'Healing isn’t just about getting stronger — it’s about unlearning the reflex to expect pain at every turn. It’s about teaching yourself that joy, too, can be familiar. That peace isn’t a trap — it’s a home you’re allowed to live in.',
            'So breathe. Let yourself unclench. When life feels still, don’t rush to fill the silence — stay there long enough for your heart to realize it’s safe.',
            'Because it is. Peace can be safe, too.',
            'If you’ve spent weeks, months, or even years surviving, peace will feel foreign at first. But keep showing up for it anyway — the same way you once showed up for survival. Because one day, your body will stop flinching at peace… and start resting in it.',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_100648553969401bb94f6076fc92ebe5~mv2.png',
    },
    {
        'old_slug': 'sometimes-it-s-ok-to-be-not-ok',
        'route': 'not-ok',
        'tag': 'Resilience',
        'title': "Sometimes It's Ok to be not Ok",
        'excerpt': 'Sometimes life just doesn’t let up. You’re already carrying more than you can handle — the deadlines, the expectations, the people depending on you — and just when you think you’re catching a break, another load drops on top. You tell yourself to keep going, but inside, you’re gasping for air. It’s not that you don’t want to be strong. You’ve been strong for too long. You ’ve carried the weight quietly, telling yourself, “I’ll be fine,” even as your chest tightens and your heart whispers,...',
        'published_date': '2025-10-28T12:47:21.164Z',
        'updated_date': '2025-10-28T12:47:21.164Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'Sometimes life just doesn’t let up. You’re already carrying more than you can handle — the deadlines, the expectations, the people depending on you — and just when you think you’re catching a break, another load drops on top. You tell yourself to keep going, but inside, you’re gasping for air.',
            'It’s not that you don’t want to be strong. You’ve been strong for too long. You’ve carried the weight quietly, telling yourself, <em>“I’ll be fine,”</em> even as your chest tightens and your heart whispers, <em>“I’m not.”</em>And the hardest part? You can’t even explain it. Because sometimes, the words don’t come. The pain feels too personal, too complicated, too heavy to share. So you stay silent. You smile in public and fall apart in private.',
            'I’ve been there. And maybe you are there now — where the weight feels unending and loneliness feels louder than your prayers.',
            'But here’s what I’ve learned: the breaking point isn’t always the end. Sometimes it’s the beginning of surrender — the point where you finally stop trying to carry everything on your own.',
            'When life feels suffocating, take one small breath. One prayer. One pause. Because healing never begins in the noise — it starts in stillness.',
            'You don’t have to have the right words to cry out to God. You don’t even need to know what to ask for. Sometimes, <em>“Help me”</em> is enough. Sometimes, the tears <em>are</em> the prayer.',
            'And if you can’t find the strength to talk to anyone, start by being honest with yourself. Say, <em>“I’m not okay right now.”</em> That truth — though small — is a doorway. It’s how the weight starts to shift.',
            'Remember: You are not weak for feeling overwhelmed. You are not faithless for being tired. You are human — and even the strongest people need to rest, to grieve, to be carried.',
            'So when everything feels too heavy, don’t rush to fix it all. Just breathe. Just rest. Just let God hold what you can’t.',
            'Because even when life feels like it’s burying you, it might actually be planting you. And in time — in His time — you’ll rise again.',
            'When was the last time you allowed yourself to stop carrying and simply <em>be held</em>?',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_6fea4f75303046a2bd780c0a23373d9d~mv2.png',
    },
    {
        'old_slug': 'when-all-seems-to-be-going-wrong',
        'route': 'when-all-goes-wrong',
        'tag': 'Faith',
        'title': 'When All Seems to Be Going Wrong',
        'excerpt': 'There are moments in life when it feels like the walls are closing in. When everything you touch seems to fall apart. When the plans you made unravel, one after another. You pray, you try, you push — but nothing seems to work. It’s in those moments that faith, purpose, and peace feel like distant echoes. When all seems to be going wrong, the temptation is to believe that something is broken — in the world, in others, or in you. But sometimes, what looks like destruction is actually...',
        'published_date': '2025-10-20T06:50:33.131Z',
        'updated_date': '2025-10-28T12:55:40.293Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'There are moments in life when it feels like the walls are closing in. When everything you touch seems to fall apart. When the plans you made unravel, one after another. You pray, you try, you push — but nothing seems to work. It’s in those moments that faith, purpose, and peace feel like distant echoes.',
            'When all seems to be going wrong, the temptation is to believe that something is broken — in the world, in others, or in you. But sometimes, what looks like destruction is actually construction in disguise. Sometimes the shaking is not to destroy you, but to rebuild you on stronger ground.',
            'I’ve learned that when things fall apart, it’s often because God is making room for something better. We can’t see it in the storm, but later we realize the storm was clearing the path. The opportunity that closed, the relationship that ended, the plan that failed — they all become part of the story that leads to growth, clarity, and strength.',
            'When life seems to be going wrong, that’s usually when we’re most tempted to give up. But that’s also when we most need to stand still. Not to fix everything, not to understand everything, but simply to <em>be still.</em> To take a breath. To look up instead of around. To remember that even when the plan doesn’t make sense, the purpose still does.',
            'Maybe you’re in that place now — where the weight feels heavy and your prayers seem unanswered. If so, hear this: You are not forgotten. You are not failing. You are simply being refined.',
            'Take small steps. Do the next right thing. Speak life over yourself even when you don’t feel it. And trust that one day, you’ll look back and realize that the things that went “wrong” were actually the things that made you strong.',
            'Because sometimes, when everything falls apart — that’s when everything starts to come together.',
            'What if this season isn’t breaking you, but shaping you? What if what feels like loss is actually the start of a new alignment?',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_bd463a0b561d48a6a6f9111113918f33~mv2.png',
    },
    {
        'old_slug': 'when-the-enemy-is-the-inner-me',
        'route': 'enemy-inner-me',
        'tag': 'Identity',
        'title': 'When the Enemy Is the Inner Me',
        'excerpt': 'Sometimes the loudest battle we fight doesn’t come from the outside — it’s the one raging quietly inside. It’s not always other people’s criticism that holds us back. It’s the voice inside that says, “You’re not good enough.” It’s not the world doubting you — it’s you doubting yourself. We often think the enemy is external, but more often than not, the real battle is internal. It’s in the false stories we tell ourselves and start believing over the truth. That voice that says, “You’ll never...',
        'published_date': '2025-10-06T06:29:11.027Z',
        'updated_date': '2025-10-28T13:00:13.887Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'Sometimes the loudest battle we fight doesn’t come from the outside — it’s the one raging quietly inside. It’s not always other people’s criticism that holds us back. It’s the voice inside that says, <em>“You’re not good enough.” </em>It’s not the world doubting you — it’s you doubting yourself.',
            'We often think the enemy is external, but more often than not, the real battle is internal. It’s in the false stories we tell ourselves and start believing over the truth.',
            'That voice that says, <em>“You’ll never change.”“ You’re too far gone.”“ You don’t have what it takes.” </em>Those are lies that take root slowly, and before long, they shape how we see ourselves, how we act, and even what we believe we deserve.',
            'The danger is that when these thoughts go unchallenged, they become our reality. We begin to live small, act scared, and settle for less because we’ve mistaken our fears for truth.',
            'But here’s the truth that never changes: You are <em>not</em> who your fears say you are. You are <em>not</em> defined by your failures. You are <em>not</em> disqualified by your past.',
            'The real truth — the one worth holding onto — says that you are created with purpose, chosen with intention, and capable of becoming everything you were designed to be.',
            'When you catch yourself speaking death over your life, pause. Ask, <em>“Would I say this to someone I love?”</em> If the answer is no, then you have no business saying it to yourself either.',
            'Replace the false words with truth.',
            'Instead of <em>“I can’t,”</em> say <em>“I’m learning.”</em>',
            'Instead of <em>“I’ve failed,”</em> say <em>“I’m growing.”</em>',
            'Instead of <em>“I’m not enough,”</em> say <em>“I’m being shaped for something greater.”</em>',
            'Victory begins the moment you stop fighting yourself and start speaking truth over your life. The real enemy loses power when you silence the inner critic and choose to believe what God says about you instead.',
            'The inner me can be my greatest enemy — but it can also become my greatest ally once I renew my mind and speak with love, grace, and truth.',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_3d8d2e7f0ad149faa8cb35016c18f3c4~mv2.png',
    },
    {
        'old_slug': 'the-power-of-thank-you',
        'route': 'the-power-of-thank-you',
        'tag': 'Gratitude',
        'title': 'The Power of Thank You',
        'excerpt': 'Gratitude is one of the simplest expressions of the heart, yet it is also one of the most powerful. We often imagine it’s reserved for big gestures—life-changing help, grand sacrifices, or milestone moments. But true gratitude lives in the small spaces of everyday life, in the ordinary moments where a simple “thank you” has the power to shift an atmosphere, soften a heart, and strengthen a bond. Think about it: when was the last time you said thank you for something small? To the colleague...',
        'published_date': '2025-10-06T06:11:33.434Z',
        'updated_date': '2025-10-28T13:05:04.193Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'Gratitude is one of the simplest expressions of the heart, yet it is also one of the most powerful. We often imagine it’s reserved for big gestures—life-changing help, grand sacrifices, or milestone moments. But true gratitude lives in the small spaces of everyday life, in the ordinary moments where a simple <em>“thank you”</em> has the power to shift an atmosphere, soften a heart, and strengthen a bond.',
            'Think about it: when was the last time you said <em>thank you</em> for something small? To the colleague who always remembers to refill the office kettle. To the spouse who takes out the trash without being asked. To the waiter who patiently gets your complicated order right. These small acknowledgements cost us nothing, yet they can mean everything to the one receiving them.',
            'I once heard someone say that gratitude is the memory of the heart. It sticks. A sincere <em>thank you</em> has a way of staying with people long after the words have been spoken. Imagine a child who proudly shows you their scribbled drawing, and instead of brushing it off, you look them in the eye and say, <em>“Thank you for sharing this with me—it’s beautiful.”</em> In that moment, you are not just encouraging them, you’re teaching them that their contribution matters.',
            'The absence of gratitude, however, leaves a void. When effort goes unnoticed, discouragement grows. A team member who works late but never hears appreciation begins to wonder if it’s worth it. A spouse who quietly holds the family together without recognition may start to feel invisible. Gratitude is not just politeness—it’s nourishment. Without it, relationships weaken.',
            'The beauty of gratitude is that it multiplies. One thank you sparks another. A culture of appreciation creates a cycle of encouragement, where people feel seen, valued, and inspired to keep giving their best.',
            'So here’s the challenge: Don’t wait for the grand moments to say thank you. Start with the little ones. Thank the driver who lets you into traffic. Thank the teacher who sends the weekly update. Thank the stranger who holds the door. Thank the friend who checks in on you with a text. These words are seeds, and over time, they grow into trust, respect, and joy.',
            'A grateful heart doesn’t just change the people around you—it changes you. Because the more you notice what’s good, the less space you have for what’s missing. Gratitude turns small moments into sacred ones.',
            'And it all begins with two simple words: <em>Thank you.</em>',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_267121fbe29845d5b212608de3cb33be~mv2.jpeg',
    },
    {
        'old_slug': 'words-that-build-not-break',
        'route': 'words-that-build-not-break',
        'tag': 'Communication',
        'title': 'Words That Build, Not Break',
        'excerpt': 'Kindness is often underestimated. We think of it as something small, something optional. Yet, the truth is, kindness has the power to shape a person’s day, or even their life. And much of that power lies in our words. Every word we speak carries weight. Some words breathe life, spark hope, and remind people of their worth. Other words cut deep, leaving wounds that aren’t easily healed. The choice is always ours: to build up or to tear down. Think about it. A simple “I believe in you” said to...',
        'published_date': '2025-10-02T10:13:11.831Z',
        'updated_date': '2025-10-28T13:10:03.490Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'Kindness is often underestimated. We think of it as something small, something optional. Yet, the truth is, kindness has the power to shape a person’s day, or even their life. And much of that power lies in our words.',
            'Every word we speak carries weight. Some words breathe life, spark hope, and remind people of their worth. Other words cut deep, leaving wounds that aren’t easily healed. The choice is always ours: to build up or to tear down.',
            'Think about it. A simple <em>“I believe in you”</em> said to a teenager struggling in school can change the way they approach their next test. A <em>“thank you, I see how hard you’re working”</em> spoken to a colleague can rekindle their motivation when they were ready to give up. Even a small <em>“you’re doing great as a mom”</em> whispered to a parent in the supermarket can turn exhaustion into renewed strength.',
            'I once saw this firsthand. A friend of mine was on the verge of leaving a project because they felt unnoticed and unappreciated. Before they could make their decision, someone from the team sent them a message that simply said: <em>“We need you. You bring something to this group no one else can.”</em> That single message stopped them from walking away. The right words, spoken at the right time, became a lifeline.',
            'Kindness is not just about the big gestures; it’s about hunting for opportunities to be a blessing in the small, everyday moments. The cashier at the supermarket',
            'who looks worn out—what if you looked them in the eye and said, <em>“Thank you for serving us with patience today.”</em> The coworker who always does the behind-the-scenes work—what if you said, <em>“I notice what you do, and it matters.”</em> The neighbor who feels invisible—what if you greeted them by name and asked how they’re doing?',
            'Our words cost us nothing, but they can give someone else courage, dignity, and strength. Proverbs says it best: <em>“The tongue has the power of life and death.”</em> When we choose life, we don’t just lift others—we lift ourselves too.',
            'So here’s the challenge: every day, look for one person to encourage, one life to bless, one heart to build up. You’ll be surprised how much difference it makes—not just in their life, but in yours.',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_d3474d8b88c749fe8a9d1a78fee744c5~mv2.jpeg',
    },
    {
        'old_slug': 'from-burden-to-blessing-shifting-the-lens-of-leadership-and-life',
        'route': 'shifting-the-lens-of-leadership-and-life',
        'tag': 'Leadership',
        'title': 'Shifting the Lens of Leadership and Life',
        'excerpt': 'It’s human nature to notice what’s missing before we recognize what’s present. We tend to measure ourselves against the gap—the things we...',
        'published_date': '2025-09-30T09:57:39.410Z',
        'updated_date': '2025-09-30T10:00:38.840Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'It’s human nature to notice what’s missing before we recognize what’s present. We tend to measure ourselves against the gap—the things we haven’t yet achieved, the goals that still feel far away, the resources we wish we had. This mindset, though common, slowly eats away at gratitude, joy, and perspective. It turns life into a constant chase instead of a gift to be lived.',
            'But what if we chose to focus on the gain instead of the gap? What if we trained ourselves to look at the blessings in our lives—the progress already made, the opportunities in front of us, and the small daily wins we so often overlook? That simple reframe changes everything. Suddenly, burdens aren’t chains but stepping stones. Struggles become classrooms. Even setbacks reveal hidden strength.',
            'Locking in a blessed mindset isn’t passive—it takes intention. It means pausing long enough to reflect on where you’ve come from, writing down three things you’re grateful for each day, and catching yourself when negativity starts to cloud your vision. It’s learning to replace <em>“I have to”</em> with <em>“I get to.”</em> It’s recognizing that every responsibility is an opportunity to serve and every challenge is a chance to grow.',
            'When you shift from burden to blessing, you unlock joy. And joy, unlike fleeting happiness, is resilient. It carries you through pressure, disappointment, and uncertainty with a quiet strength. Joyful service—whether to your family, your team, or your calling—breathes life into everyone around you.',
            'Leadership, after all, is less about carrying the heaviest load and more about how you carry it. A blessed mindset allows you to serve not out of obligation but out of gratitude. And that spirit of gratitude is contagious. When others see you choosing joy in the face of challenges, it gives them permission to do the same.',
            'So the next time life tries to weigh you down with its burdens, pause. Ask yourself: <em>Am I staring at the gap, or am I celebrating the gain?</em> Choose to see the blessing, and watch how it transforms not only your perspective, but also the people you lead.',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_7c7585ad4f3a4e8096c2ae81dd33595c~mv2.jpg',
    },
    {
        'old_slug': 'when-the-leader-runs-empty',
        'route': 'when-the-leader-runs-empty',
        'tag': 'Leadership',
        'title': 'When the Leader Runs Empty',
        'excerpt': 'There are days when leadership feels heavy. Not because of the workload or the deadlines, but because the spark inside you has dimmed....',
        'published_date': '2025-09-26T07:33:45.394Z',
        'updated_date': '2025-09-26T07:33:45.394Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'There are days when leadership feels heavy. Not because of the workload or the deadlines, but because the spark inside you has dimmed. You wake up with no energy, no drive, and no desire to push forward. The hardest part is that you notice it spilling into your team. Their energy mirrors yours. Their pace slows down. The room feels heavier, and deep down you know it has everything to do with what you’re carrying.',
            'But you’re stuck. You know you should do something, yet the very thought of fixing it feels exhausting. So, instead of addressing it, you leave things as they are, hoping somehow they’ll get better on their own.',
            'I’ve been there. And maybe you have too.',
            'The truth is, leadership isn’t about always being strong. It’s about being human, and sometimes humanity comes with emptiness. The danger, however, is when we stay there. A demotivated leader can quietly pull an entire team into survival mode without ever saying a word. Our silence speaks. Our disengagement echoes. And the longer we remain motionless, the more we communicate: <em>this is acceptable.</em>',
            'So what do you do when you have nothing left to give?',
            'First, you admit it. Leadership doesn’t mean faking strength; it means modeling honesty. Sometimes the most powerful thing you can say to your team is: <em>“I’m not at my best right now, but I’m committed to finding a way through this.”</em> That small act of vulnerability can reset the atmosphere because it shifts the weight from hidden tension to shared understanding.',
            'Second, you take one small step. Not ten. Not the whole mountain. Just one. Maybe it’s reaching out to a mentor, stepping outside for fresh air, or writing down the one thing that matters today. Momentum doesn’t begin with giant leaps — it starts with the tiniest movement forward.',
            'Finally, you remind yourself that your energy doesn’t come from you alone. Leadership that tries to run on empty will always burn out. But leadership rooted in faith, in something deeper than yourself, has a source that never runs dry. <em>“Those who hope in the Lord will renew their strength. They will soar on wings like eagles”</em> (Isaiah 40:31).',
            'If you find yourself empty today, know this: you are not alone, and this moment does not define you. Leadership isn’t about never running out — it’s about choosing to reach for renewal when you do. Your team doesn’t need you to be superhuman. They need you to be real, to keep showing up, and to keep daring, even in weakness, to take one more step forward.',
            '<em>What’s one small step you can take today to shift the weight and renew your strength?</em>',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_63ffcb40f7064ccb965b3d532f9912b0~mv2.png',
    },
    {
        'old_slug': 'pressure-reveals-the-leader',
        'route': 'pressure-reveals-the-leader',
        'tag': 'Leadership',
        'title': 'Pressure Reveals the Leader',
        'excerpt': 'Anyone can look like a leader when life is easy. When the sun is shining, the team is winning, and everything is falling neatly into place, leadership doesn’t cost much. But the true measure of leadership is not revealed in calm waters — it comes to light in the storm. Pressure has a way of stripping away pretense, exposing what we really carry inside, and showing whether our leadership is built on sand or on rock. In moments of trouble, people don’t need polished words or rehearsed...',
        'published_date': '2025-09-23T07:00:09.304Z',
        'updated_date': '2025-10-28T13:20:21.334Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'Anyone can look like a leader when life is easy. When the sun is shining, the team is winning, and everything is falling neatly into place, leadership doesn’t cost much. But the true measure of leadership is not revealed in calm waters — it comes to light in the storm. Pressure has a way of stripping away pretense, exposing what we really carry inside, and showing whether our leadership is built on sand or on rock.',
            'In moments of trouble, people don’t need polished words or rehearsed confidence. They look for steadiness. They look for a leader whose faith doesn’t collapse under weight, whose character isn’t for sale, and whose presence brings calm instead of chaos. That’s when leadership speaks for itself, without titles, without applause.',
            'Jesus showed us this on the night before His crucifixion. While His disciples panicked, argued, and even ran away, He chose calm surrender. In His moment of greatest pressure, He knelt to pray, anchored Himself in the Father’s will, and still thought of serving others — even washing feet. The cross didn’t silence His leadership; it revealed it.',
            'The truth is, trouble always comes. The question is not if, but when. And when it does, it magnifies what’s inside us. If fear, pride, or insecurity are at the core, they’ll spill out quickly. But if faith, character, and servant-hearted strength are at the center, that too will be revealed. Pressure doesn’t create leaders — it reveals them.',
            'So if you feel like you’re in the middle of a storm, don’t see it as the end of your leadership. See it as the proving ground. This is the place where you become unshakable. Where the quiet work you’ve done in building faith and integrity shows its worth. Where your life speaks louder than any speech you could give.',
            'When the storm passes — and it always does — people will remember not the size of the trouble, but the steadiness of the leader who walked them through it.',
            '<em>When the pressure is on, what will your leadership reveal?</em>',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_7bb31f0b3ef24a9fb2a1c5131555c9a4~mv2.jpeg',
    },
    {
        'old_slug': 'dare-to-lead',
        'route': 'dare-to-lead',
        'tag': 'Leadership',
        'title': 'Dare to Lead',
        'excerpt': 'Leadership is one of the most misunderstood words in our world today. Too often, people think it belongs only to CEOs, politicians, or...',
        'published_date': '2025-09-22T14:30:39.112Z',
        'updated_date': '2025-09-22T14:32:12.326Z',
        'minutes_to_read': 2,
        'html_paragraphs': [
            'Leadership is one of the most misunderstood words in our world today. Too often, people think it belongs only to CEOs, politicians, or those with big platforms. But the truth is, leadership isn’t about position — it’s about responsibility. Each of us is leading somewhere, whether in our families, our communities, or simply through the way we live our lives. To lead is to influence, and to influence is to take responsibility for the impact of our choices. That’s why I call this <em>Dare to Lead</em> — because leadership requires courage.',
            'It takes courage to serve. Jesus redefined greatness when He said, <em>“The greatest among you will be your servant.”</em> Real leadership isn’t measured by how many serve you, but by how many you serve. Serving means putting others first when it’s inconvenient, choosing humility over pride, and lifting people up when you’d rather focus on yourself. The world says power is control, but Christ teaches that true power is found in surrender.',
            'It also takes courage to be different. It’s easy to follow the crowd, to live by the standards everyone else accepts. But leaders are called to higher ground. Romans reminds us not to conform to the patterns of this world but to be transformed by renewing our minds. To lead means being willing to walk away from comfort zones, to speak truth when silence would be easier, and sometimes to walk alone when others choose the wide road.',
            'And yes, it takes courage to fail. Real leaders stumble. They make mistakes. They fall. But what sets them apart is the willingness to rise again, to learn from what went wrong, and to keep moving forward. Failure isn’t the end of leadership — it’s a part of it. Every time you rise again, you prove that courage isn’t about never falling, but about never quitting.',
            'You don’t need a title to lead. You don’t need a stage, a corner office, or a large following. All you need is the courage to step forward. Courage to serve, courage to be different, courage to rise again. When you dare to lead in your home, in your workplace, or in your community, you become living proof of what God can do through an ordinary person with extraordinary faith.',
            'Leadership is not about waiting for the perfect moment. It’s about daring to take the step today.',
            'So let me leave you with this: where is God calling you to dare to lead right now?',
        ],
        'image_url': 'https://static.wixstatic.com/media/366a4f_3ff10438c30f4ae691da24075dfb13db~mv2.jpg',
    },
]


def run_curl(url: str, *, headers: dict[str, str] | None = None, method: str = "GET", data: str | None = None, resolve_old: bool = False) -> str:
    handle, output_path = tempfile.mkstemp(prefix="munya-wix-", suffix=".json")
    os.close(handle)
    args = ["curl.exe", "-sS", "-L", "--output", output_path]
    if resolve_old:
        args.extend(["-k", "--resolve", f"{OLD_HOST}:443:{OLD_IP}"])
    for name, value in (headers or {}).items():
        args.extend(["-H", f"{name}: {value}"])
    if method != "GET":
        args.extend(["-X", method])
    if data is not None:
        args.extend(["--data-binary", data])
    args.append(url)
    try:
        subprocess.run(args, check=True, capture_output=True, text=True, encoding="utf-8")
        return Path(output_path).read_text(encoding="utf-8")
    finally:
        Path(output_path).unlink(missing_ok=True)


def fetch_json(url: str, **kwargs) -> dict:
    return json.loads(run_curl(url, **kwargs))


def fetch_access_token() -> str:
    payload = fetch_json(f"https://{OLD_HOST}/_api/v1/access-tokens", resolve_old=True)
    return payload["apps"][BLOG_APP_ID]["accessToken"]


def fetch_posts(access_token: str) -> list[dict]:
    listing = fetch_json(
        "https://www.wixapis.com/blog/v3/posts?paging.limit=100",
        headers={"Authorization": access_token},
    )["posts"]
    detailed_posts = []

    for listed_post in listing:
        query = json.dumps(
            {
                "dataCollectionId": "Blog/Posts",
                "query": {"filter": {"slug": {"$eq": listed_post["slug"]}}},
            }
        )
        item = fetch_json(
            "https://www.wixapis.com/wix-data/v2/items/query",
            method="POST",
            data=query,
            headers={
                "Authorization": access_token,
                "Content-Type": "application/json",
            },
        )["dataItems"][0]["data"]

        config = POST_CONFIG[listed_post["slug"]]
        detailed_posts.append(
            {
                "old_slug": listed_post["slug"],
                "route": config["route"],
                "tag": config["tag"],
                "title": listed_post["title"],
                "excerpt": clean_excerpt(item.get("excerpt") or listed_post.get("excerpt") or ""),
                "published_date": item["publishedDate"]["$date"],
                "updated_date": item["lastPublishedDate"]["$date"],
                "minutes_to_read": int(round(item.get("timeToRead") or listed_post.get("minutesToRead") or 2)),
                "plain_content": item.get("plainContent", "").strip(),
                "rich_content": item.get("richContent", {}).get("nodes", []),
                "image_url": listed_post.get("media", {})
                .get("wixMedia", {})
                .get("image", {})
                .get("url", f"{SITE_URL}/assets/images/munya-home.jpg"),
            }
        )

    detailed_posts.sort(key=lambda post: post["published_date"], reverse=True)
    return detailed_posts


def decode_html_entities(text: str) -> str:
    text = str(text)
    for _ in range(3):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded
    return text


def clean_excerpt(text: str) -> str:
    text = normalize_text(text)
    text = " ".join(text.replace("\u00a0", " ").split())
    return text.replace("You ’re", "You’re").replace("you  ", "you ").replace("thank you  ", "thank you ").strip()


def normalize_text(text: str, *, strip_edges: bool = True) -> str:
    text = decode_html_entities(text)
    text = text.replace("\u00a0", " ")
    leading_space = text[:1].isspace()
    trailing_space = text[-1:].isspace()
    text = re.sub(r"([.!?])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([.!?])([“\"'])", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    if not strip_edges:
        if leading_space:
            text = f" {text}"
        if trailing_space:
            text = f"{text} "
    return text


def escape_text(text: str, *, strip_edges: bool = True) -> str:
    return html.escape(normalize_text(text, strip_edges=strip_edges), quote=False)


def escape_attr(text: str, *, strip_edges: bool = True) -> str:
    # Double-quoted attributes only need double quotes escaped; apostrophes should
    # remain readable so they never appear on-page as encoded leftovers.
    return html.escape(normalize_text(text, strip_edges=strip_edges), quote=True).replace("&#x27;", "'")


def format_date(value: str) -> str:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    return f"{dt.day} {dt.strftime('%B %Y')}"


def iso_date(value: str) -> str:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()


def reading_time_label(minutes: int) -> str:
    return f"{minutes} min read"


def text_snippet(text: str, limit: int) -> str:
    text = clean_excerpt(text)
    if len(text) <= limit:
        return text
    sliced = text[:limit].rsplit(" ", 1)[0].strip()
    return f"{sliced}..."


def render_inline_node(node: dict) -> str:
    node_type = node.get("type")
    if node_type == "TEXT":
        rendered = escape_text(node.get("textData", {}).get("text", ""), strip_edges=False)
        for decoration in node.get("textData", {}).get("decorations", []):
            deco_type = decoration.get("type")
            if deco_type == "ITALIC":
                rendered = f"<em>{rendered}</em>"
            elif deco_type == "BOLD":
                rendered = f"<strong>{rendered}</strong>"
        return rendered

    children = "".join(render_inline_node(child) for child in node.get("nodes", []))
    if node_type == "LINK":
        link = node.get("linkData", {}).get("link", {})
        url = link.get("url")
        if url:
            return f'<a href="{escape_attr(url)}" target="_blank" rel="noopener">{children}</a>'
    return children


def paragraph_text(post: dict) -> list[str]:
    if post.get("html_paragraphs"):
        # Pre-rendered HTML paragraphs (e.g. migrated legacy posts that still
        # carry inline <em>/<strong>/<a> tags). They are emitted verbatim, so
        # do NOT pass through escape_text or the should_join_paragraph merge.
        return [paragraph for paragraph in post["html_paragraphs"] if paragraph.strip()]
    if post.get("paragraphs"):
        return [escape_text(paragraph) for paragraph in post["paragraphs"] if paragraph.strip()]

    paragraphs: list[str] = []
    for node in post["rich_content"]:
        if node.get("type") != "PARAGRAPH":
            continue
        content = "".join(render_inline_node(child) for child in node.get("nodes", []))
        content = content.strip()
        if content:
            paragraphs.append(content)
    if paragraphs:
        merged: list[str] = []
        for paragraph in paragraphs:
            if merged and should_join_paragraph(merged[-1], paragraph):
                merged[-1] = f"{merged[-1]} {paragraph}"
            else:
                merged.append(paragraph)
        return merged
    fallback = clean_excerpt(post["plain_content"])
    return [escape_text(fallback)] if fallback else []


def strip_markup(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def should_join_paragraph(previous: str, current: str) -> bool:
    prev_plain = strip_markup(previous).strip()
    curr_plain = strip_markup(current).strip()
    if not prev_plain or not curr_plain:
        return False
    if prev_plain[-1] in ".!?;:”\"'":
        return False
    return bool(re.match(r"^(and|or|but|because|so|that|it|you|we|they|the|a|an)\b", curr_plain, flags=re.IGNORECASE))


def first_paragraph_plain(post: dict) -> str:
    paragraphs = paragraph_text(post)
    if not paragraphs:
        return ""
    plain = (
        paragraphs[0]
        .replace("<em>", "")
        .replace("</em>", "")
        .replace("<strong>", "")
        .replace("</strong>", "")
    )
    return clean_excerpt(plain)


def summary_source(post: dict) -> str:
    return clean_excerpt(post.get("summary") or first_paragraph_plain(post) or post["excerpt"])


def render_article_body(post: dict) -> str:
    paragraphs = paragraph_text(post)
    blocks = []
    for index, paragraph in enumerate(paragraphs):
        class_attr = ' class="lead"' if index == 0 else ""
        blocks.append(f"<p{class_attr}>{paragraph}</p>")
    return "\n          ".join(blocks)


def post_audio_url(post: dict) -> str:
    if post.get("audio_url"):
        return str(post["audio_url"])
    audio_path = AUDIO_DIR / f"{post['route']}.mp3"
    if audio_path.exists():
        return f"/assets/audio/{post['route']}.mp3"
    return ""


def render_audio_player(post: dict) -> str:
    audio_url = post_audio_url(post)
    if not audio_url:
        return ""

    title = escape_attr(post["title"])
    route = escape_attr(post["route"])
    return f"""
        <div class="post-audio" data-audio-player data-audio-route="{route}">
          <button class="audio-toggle" type="button" data-audio-toggle aria-label="Listen to {title}" aria-pressed="false">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M8 5v14l11-7L8 5Z"></path>
            </svg>
            <span data-audio-label>Listen to this reflection</span>
          </button>
          <audio class="audio-control" controls preload="none" src="{escape_attr(audio_url)}">
            Your browser does not support audio playback.
          </audio>
        </div>"""


def article_description(post: dict) -> str:
    return text_snippet(summary_source(post), 158)


def article_intro(post: dict) -> str:
    return text_snippet(summary_source(post), 210)


def page_route(page_number: int) -> str:
    return "/writing" if page_number == 1 else f"/writing/page/{page_number}"


def page_title(page_number: int) -> str:
    return "Writing | Munya Chipunza" if page_number == 1 else f"Writing Page {page_number} | Munya Chipunza"


def archive_canonical(page_number: int) -> str:
    return f"{SITE_URL}{page_route(page_number)}"


def header(active: str, cta_href: str, cta_label: str) -> str:
    return f"""    <header class="site-header">
      <div class="nav-shell">
        <a class="brand-mark" href="/">
          <strong>Munya</strong>
          <span>Chipunza</span>
        </a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Toggle navigation" data-nav-toggle>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">
            <path d="M4 7h16M4 12h16M4 17h16"></path>
          </svg>
        </button>
        <ul class="nav-links" data-nav-links>
          <li><a href="/"{' class="active"' if active == "home" else ""}>Home</a></li>
          <li><a href="/about"{' class="active"' if active == "about" else ""}>About</a></li>
          <li><a href="/writing"{' class="active"' if active == "writing" else ""}>Writing</a></li>
          <li><a href="/shop"{' class="active"' if active == "shop" else ""}>Shop</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
        <div class="nav-actions">
          <a class="button button-secondary" href="{cta_href}">{cta_label}</a>
        </div>
      </div>
    </header>"""


FOOTER = """    <footer class="footer">
      <div class="footer-shell">
        <div class="footer-grid">
          <div>
            <strong>Munya Chipunza</strong>
            <p>Reflections on faith, resilience, and hope for anyone navigating a season that feels heavier than expected.</p>
          </div>
          <div>
            <div class="footer-heading">Navigate</div>
            <div class="footer-links">
              <a href="/">Home</a>
              <a href="/about">About</a>
              <a href="/writing">Writing</a>
              <a href="/shop">Shop</a>
            </div>
          </div>
          <div>
            <div class="footer-heading">Elsewhere</div>
            <div class="footer-social">
              <a class="social-link" href="https://www.facebook.com/chipunzamunya" target="_blank" rel="noopener" aria-label="Facebook">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"></path></svg>
              </a>
              <a class="social-link" href="https://www.instagram.com/iam_munya/" target="_blank" rel="noopener" aria-label="Instagram">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"></path></svg>
              </a>
              <a class="social-link" href="https://www.linkedin.com/in/munya-chipunza-73a1a039/" target="_blank" rel="noopener" aria-label="LinkedIn">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.447 20.452H16.893V14.87c0-1.333-.027-3.045-1.856-3.045-1.858 0-2.142 1.45-2.142 2.948v5.68H9.34V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.124 2.062 2.062 0 0 1 0 4.124zM7.119 20.452H3.555V9H7.12v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path></svg>
              </a>
              <a class="social-link" href="https://x.com/Iam_munya" target="_blank" rel="noopener" aria-label="X">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"></path></svg>
              </a>
              <a class="social-link" href="https://www.tiktok.com/@munyachipunza" target="_blank" rel="noopener" aria-label="TikTok">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"></path></svg>
              </a>
              <a class="social-link" href="https://www.threads.com/@iam_munya" target="_blank" rel="noopener" aria-label="Threads">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 0 1 3.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.586-1.308-.883-2.359-.89h-.029c-.844 0-1.992.232-2.721 1.32L7.734 7.847c.98-1.454 2.568-2.256 4.478-2.256h.044c3.194.02 5.097 1.975 5.287 5.388.108.046.216.094.321.142 1.49.7 2.58 1.761 3.154 3.07.797 1.82.871 4.79-1.548 7.158-1.85 1.81-4.094 2.628-7.277 2.65Zm1.003-11.69c-.242 0-.487.007-.739.021-1.836.103-2.98.946-2.916 2.143.067 1.256 1.452 1.839 2.784 1.767 1.224-.065 2.818-.543 3.086-3.71a10.5 10.5 0 0 0-2.215-.221z"></path></svg>
              </a>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <span>&copy; <span data-year></span> Munya Chipunza.</span>
          <span>Written in Cape Town, rooted in Zimbabwe.</span>
        </div>
      </div>
    </footer>"""


def contact_form_fields(subject: str, source: str = "contact") -> str:
    return f"""          <form class="signup-form full" name="contact" method="POST" action="{CONTACT_FORM_ACTION}" data-contact-form data-form-provider="{CONTACT_FORM_PROVIDER}" data-ajax-action="{CONTACT_FORM_AJAX}" data-mailto-fallback="{CONTACT_EMAIL}" data-analytics-source="{escape_attr(source)}" data-success-message="Thank you. Your message has reached me privately." data-success-button-label="Message sent" id="contact-form">
            <input type="hidden" name="access_key" value="{WEB3FORMS_ACCESS_KEY}">
            <input type="hidden" name="subject" value="{escape_attr(subject)}">
            <input type="hidden" name="_subject" value="{escape_attr(subject)}">
            <input type="hidden" name="from_name" value="MunyaChipunza.com">
            <input type="hidden" name="redirect" value="{CONTACT_SUCCESS_URL}">
            <p class="sr-only">
              <label>Leave this field empty <input name="botcheck" tabindex="-1" autocomplete="off"></label>
            </p>
            <input type="text" name="name" placeholder="Your name" autocomplete="name" required>
            <input type="email" name="email" placeholder="Your email address" autocomplete="email" required>
            <textarea class="full-row" name="message" placeholder="Your message" required></textarea>
            <button class="button button-primary full-row" type="submit">Send message</button>
          </form>
          <p class="form-note" data-form-status aria-live="polite">Your note sends privately from this page.</p>"""


def subscribe_form_fields(subject: str, source: str) -> str:
    if SUBSCRIBE_MODE == "buttondown":
        return f"""          <form class="signup-form subscribe-form" name="subscribe" method="POST" action="{BUTTONDOWN_SUBSCRIBE_ACTION}" data-subscribe-form data-analytics-source="{escape_attr(source)}">
            <input type="hidden" value="1" name="embed">
            <input type="hidden" name="metadata__source" value="{escape_attr(source)}">
            <input type="email" name="email" placeholder="Your email address" autocomplete="email" aria-label="Your email address" required>
            <button class="button button-primary" type="submit">Subscribe</button>
          </form>
          <p class="form-note" data-form-status aria-live="polite">Occasional reflections. Please check your inbox to confirm.</p>"""

    if SUBSCRIBE_MODE == "holding":
        return f"""          <form class="signup-form subscribe-form" name="subscribe" method="POST" action="{CONTACT_FORM_ACTION}" data-subscribe-form data-form-provider="{CONTACT_FORM_PROVIDER}" data-ajax-action="{CONTACT_FORM_AJAX}" data-analytics-source="{escape_attr(source)}" data-pending-message="Saving your subscription..." data-success-message="Thank you. You're on the list." data-success-button-label="Subscribed">
            <input type="hidden" name="access_key" value="{WEB3FORMS_ACCESS_KEY}">
            <input type="hidden" name="subject" value="{escape_attr(subject)}">
            <input type="hidden" name="_subject" value="{escape_attr(subject)}">
            <input type="hidden" name="from_name" value="MunyaChipunza.com">
            <input type="hidden" name="form_type" value="newsletter_subscription">
            <input type="hidden" name="status" value="holding until Buttondown account review is approved">
            <input type="hidden" name="interest" value="New reflections by email">
            <input type="hidden" name="source" value="{escape_attr(source)}">
            <p class="sr-only">
              <label>Leave this field empty <input name="botcheck" tabindex="-1" autocomplete="off"></label>
            </p>
            <input type="email" name="email" placeholder="Your email address" autocomplete="email" aria-label="Your email address" required>
            <button class="button button-primary" type="submit">Subscribe</button>
          </form>
          <p class="form-note" data-form-status aria-live="polite">Occasional reflections. No noise.</p>"""

    raise ValueError(f"Unsupported SUBSCRIBE_MODE: {SUBSCRIBE_MODE}")


def render_subscribe_section(title: str, description: str, source: str) -> str:
    return f"""      <section class="subscribe-section">
        <div class="subscribe-panel will-reveal">
          <div class="subscribe-copy">
            <p class="eyebrow">By email</p>
            <h2>{escape_text(title)}</h2>
            <p>{escape_text(description)}</p>
          </div>
          <div class="subscribe-form-shell">
{subscribe_form_fields("New writing subscriber from munyachipunza.com", source)}
          </div>
        </div>
      </section>"""


FORM_SECTION = f"""      <section class="form-section" id="contact">
        <div class="form-panel will-reveal">
          <p class="eyebrow">Stay in touch</p>
          <h2>Send a note.</h2>
          <p>If something in the writing met you where you are, this is the simplest way to reach out.</p>
{contact_form_fields("New message from munyachipunza.com")}
        </div>
      </section>"""


def archive_cards(posts: list[dict]) -> str:
    cards = []
    for post in posts:
        cards.append(
            f"""        <a class="article-card will-reveal" href="/writing/{post["route"]}">
          <div>
            <p class="article-tag">{escape_text(post["tag"])}</p>
            <h2 class="article-card-title">{escape_text(post["title"])}</h2>
            <p>{escape_text(text_snippet(post["excerpt"] or first_paragraph_plain(post), 260))}</p>
          </div>
          <div class="article-meta">
            <div>{format_date(post["published_date"])}</div>
            <div>{reading_time_label(post["minutes_to_read"])}</div>
          </div>
        </a>"""
        )
    return "\n\n".join(cards)


def render_pagination(page_number: int, total_pages: int) -> str:
    page_links = []
    for number in range(1, total_pages + 1):
        if number == page_number:
            page_links.append(f'<span class="pagination-link is-current" aria-current="page">{number}</span>')
        else:
            page_links.append(f'<a class="pagination-link" href="{page_route(number)}">{number}</a>')

    previous_link = (
        f'<a class="pagination-button" href="{page_route(page_number - 1)}">Newer page</a>'
        if page_number > 1
        else '<span class="pagination-button is-disabled">Newer page</span>'
    )
    next_link = (
        f'<a class="pagination-button" href="{page_route(page_number + 1)}">Older page</a>'
        if page_number < total_pages
        else '<span class="pagination-button is-disabled">Older page</span>'
    )

    return f"""      <nav class="pagination" aria-label="Writing pages">
        <div class="pagination-row">
          {previous_link}
          <span class="pagination-label">Page {page_number} of {total_pages}</span>
          {next_link}
        </div>
        <div class="pagination-links">
          {' '.join(page_links)}
        </div>
      </nav>"""


def render_archive_page(page_posts: list[dict], page_number: int, total_pages: int, total_posts: int) -> str:
    title = page_title(page_number)
    description = SITE_DESCRIPTION
    hero_line = "Short reflections on faith, identity, grief, peace, and the quiet interior work required to stay human under pressure."
    page_note = f"Page {page_number} of {total_pages} &middot; {total_posts} published reflections."
    canonical = archive_canonical(page_number)
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_text(title)}</title>
    <meta name="description" content="{escape_attr(description)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{escape_attr(title)}">
    <meta property="og:description" content="{escape_attr(description)}">
    <meta property="og:site_name" content="Munya Chipunza">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{SITE_URL}/assets/images/munya-home.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape_attr(title)}">
    <meta name="twitter:description" content="{escape_attr(description)}">
    <meta name="twitter:image" content="{SITE_URL}/assets/images/munya-home.jpg">
    <link rel="alternate" href="{SITE_URL}/blog-feed.xml" title="Munya Chipunza - RSS" type="application/rss+xml">
{ICON_LINKS}
    <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="/assets/css/style.css">
{GOOGLE_ANALYTICS_TAG}
  </head>
  <body>
{header("writing", "/about", "About Munya")}

    <main>
      <section class="page-hero">
        <p class="eyebrow">All writing</p>
        <h1>Words for the road.</h1>
        <p>{hero_line}</p>
        <p class="archive-note">{page_note}</p>
      </section>

      <section class="article-list">
{archive_cards(page_posts)}
      </section>

{render_pagination(page_number, total_pages)}

{render_subscribe_section("Get new reflections by email.", "Prefer email to scrolling? Join the list and I'll send the next reflection quietly when it is ready.", f"writing archive page {page_number}")}

{FORM_SECTION}
    </main>

{FOOTER}

    <script src="/assets/js/site.js?v={ASSET_VERSION}"></script>
  </body>
</html>
"""


def render_article_nav(posts: list[dict], index: int) -> str:
    newer = posts[index - 1] if index > 0 else None
    older = posts[index + 1] if index + 1 < len(posts) else None

    left = (
        f"""        <a href="/writing/{newer["route"]}">
          <span>Newer reflection</span>
          <strong>{escape_text(newer["title"])}</strong>
        </a>"""
        if newer
        else "        <div></div>"
    )
    right = (
        f"""        <a href="/writing/{older["route"]}">
          <span>Older reflection</span>
          <strong>{escape_text(older["title"])}</strong>
        </a>"""
        if older
        else "        <div></div>"
    )

    return f"""      <nav class="article-nav">
{left}
{right}
      </nav>"""


def render_engagement_section(post: dict, canonical: str) -> str:
    title = post["title"]
    route = escape_attr(post["route"])
    source = f"article note: {post['route']}"
    share_title = quote(f"{post['title']} by Munya Chipunza")
    share_url = quote(canonical, safe="")
    return f"""      <section class="engagement-section quiet-response-section" id="responses" aria-labelledby="response-title">
        <div class="quiet-response-panel will-reveal">
          <div class="quiet-response-intro">
            <p class="eyebrow">After reading</p>
            <h2 id="response-title">Stay with the reflection</h2>
            <p>If this piece met you where you are, there are two quiet ways to respond. You can share it with someone who may need the words, or you can send a private note in plain words. No public comment section. No performance. Just a small response if something here stayed with you.</p>
          </div>

          <div class="quiet-response-grid">
            <article class="quiet-response-card">
              <h3>Share this reflection</h3>
              <p>Send it to someone who may need the words today.</p>
              <div class="quiet-share-actions" aria-label="Share this reflection">
                <button class="quiet-share-action quiet-copy-action" type="button" data-copy-link="{escape_attr(canonical)}" data-share-platform="copy_link" aria-label="Copy article link" title="Copy article link">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 7a3 3 0 0 1 3-3h6a3 3 0 0 1 0 6h-2v-2h2a1 1 0 1 0 0-2h-6a1 1 0 1 0 0 2v2a3 3 0 0 1-3-3Zm6 10a3 3 0 0 1-3 3H6a3 3 0 1 1 0-6h2v2H6a1 1 0 1 0 0 2h6a1 1 0 1 0 0-2v-2a3 3 0 0 1 3 3Zm-8-4h10v-2H7v2Z"></path></svg>
                  <span data-copy-text>Copy link</span>
                </button>
                <a class="quiet-share-action quiet-share-icon" href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" rel="noopener" data-share-platform="facebook" aria-label="Share on Facebook" title="Share on Facebook">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"></path></svg>
                </a>
                <a class="quiet-share-action quiet-share-icon" href="https://twitter.com/intent/tweet?text={share_title}&amp;url={share_url}" target="_blank" rel="noopener" data-share-platform="x" aria-label="Share on X" title="Share on X">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"></path></svg>
                </a>
                <a class="quiet-share-action quiet-share-icon" href="https://www.threads.com/intent/post?text={share_title}%20{share_url}" target="_blank" rel="noopener" data-share-platform="threads" aria-label="Share on Threads" title="Share on Threads">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.186 24h-.007c-3.581-.024-6.334-1.205-8.184-3.509C2.35 18.44 1.5 15.586 1.472 12.01v-.017c.03-3.579.879-6.43 2.525-8.482C5.845 1.205 8.6.024 12.18 0h.014c2.746.02 5.043.725 6.826 2.098 1.677 1.29 2.858 3.13 3.509 5.467l-2.04.569c-1.104-3.96-3.898-5.984-8.304-6.015-2.91.022-5.11.936-6.54 2.717C4.307 6.504 3.616 8.914 3.589 12c.027 3.086.718 5.496 2.057 7.164 1.43 1.783 3.631 2.698 6.54 2.717 2.623-.02 4.358-.631 5.8-2.045 1.647-1.613 1.618-3.593 1.09-4.798-.31-.71-.873-1.3-1.634-1.75-.192 1.352-.622 2.446-1.284 3.272-.886 1.102-2.14 1.704-3.73 1.79-1.202.065-2.361-.218-3.259-.801-1.063-.689-1.685-1.74-1.752-2.964-.065-1.19.408-2.285 1.33-3.082.88-.76 2.119-1.207 3.583-1.291a13.853 13.853 0 0 1 3.02.142c-.126-.742-.375-1.332-.75-1.757-.513-.586-1.308-.883-2.359-.89h-.029c-.844 0-1.992.232-2.721 1.32L7.734 7.847c.98-1.454 2.568-2.256 4.478-2.256h.044c3.194.02 5.097 1.975 5.287 5.388.108.046.216.094.321.142 1.49.7 2.58 1.761 3.154 3.07.797 1.82.871 4.79-1.548 7.158-1.85 1.81-4.094 2.628-7.277 2.65Zm1.003-11.69c-.242 0-.487.007-.739.021-1.836.103-2.98.946-2.916 2.143.067 1.256 1.452 1.839 2.784 1.767 1.224-.065 2.818-.543 3.086-3.71a10.5 10.5 0 0 0-2.215-.221z"></path></svg>
                </a>
                <a class="quiet-share-action quiet-share-icon" href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" target="_blank" rel="noopener" data-share-platform="linkedin" aria-label="Share on LinkedIn" title="Share on LinkedIn">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.447 20.452H16.893V14.87c0-1.333-.027-3.045-1.856-3.045-1.858 0-2.142 1.45-2.142 2.948v5.68H9.34V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.124 2.062 2.062 0 0 1 0 4.124zM7.119 20.452H3.555V9H7.12v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path></svg>
                </a>
                <button class="quiet-share-action quiet-native-share" type="button" hidden data-native-share data-share-url="{escape_attr(canonical)}" data-share-title="{escape_attr(title)}" data-share-platform="native" aria-label="Share this reflection" title="Share this reflection">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7a3.3 3.3 0 0 0 0-1.39l7.05-4.11A3 3 0 1 0 15 5c0 .23.03.45.08.67L8.03 9.78a3 3 0 1 0 0 4.44l7.12 4.16c-.05.2-.07.41-.07.62a2.92 2.92 0 1 0 2.92-2.92Z"></path></svg>
                  <span>Share</span>
                </button>
              </div>
              <p class="quiet-share-note">Instagram and TikTok work best through the share button on mobile, or by copying the link and pasting it there.</p>
            </article>

            <article class="quiet-response-card quiet-note-card">
              <h3>Send a private note</h3>
              <p>If this reflection met you where you are, you can respond in plain words. Your note comes through privately and lands in my inbox.</p>
              <form class="signup-form full response-form quiet-note-form" name="private-note" method="POST" action="{CONTACT_FORM_ACTION}" data-contact-form data-form-provider="{CONTACT_FORM_PROVIDER}" data-ajax-action="{CONTACT_FORM_AJAX}" data-mailto-fallback="{CONTACT_EMAIL}" data-analytics-source="{escape_attr(source)}" data-pending-message="Sending your private note..." data-success-message="Thank you. Your note has reached me privately." data-error-message="The note could not send from the website. Please try again, or email hello@munyachipunza.com directly." data-success-button-label="Note sent" data-error-button-label="Try again">
                <input type="hidden" name="access_key" value="{WEB3FORMS_ACCESS_KEY}">
                <input type="hidden" name="subject" value="{escape_attr(f'Private note about {title}')}">
                <input type="hidden" name="_subject" value="{escape_attr(f'Private note about {title}')}">
                <input type="hidden" name="from_name" value="MunyaChipunza.com">
                <input type="hidden" name="redirect" value="{CONTACT_SUCCESS_URL}">
                <input type="hidden" name="form_type" value="private_note">
                <input type="hidden" name="article_title" value="{escape_attr(title)}">
                <input type="hidden" name="article_url" value="{escape_attr(canonical)}">
                <div class="sr-only" aria-hidden="true">
                  <label>Leave this field empty <input name="botcheck" tabindex="-1" autocomplete="off"></label>
                </div>
                <div class="form-field">
                  <label class="field-label" for="note-name-{route}">Name</label>
                  <input id="note-name-{route}" type="text" name="name" placeholder="Name" autocomplete="name" required>
                </div>
                <div class="form-field">
                  <label class="field-label" for="note-email-{route}">Email address</label>
                  <input id="note-email-{route}" type="email" name="email" placeholder="Email address" autocomplete="email" required>
                </div>
                <div class="form-field full-row">
                  <label class="field-label" for="note-message-{route}">Message</label>
                  <textarea id="note-message-{route}" name="message" placeholder="Message" required></textarea>
                </div>
                <button class="button button-primary full-row" type="submit">Send note</button>
              </form>
              <p class="form-note" data-form-status aria-live="polite">Your note sends privately from this page.</p>
            </article>
          </div>
        </div>
      </section>"""


def render_article_page(post: dict, posts: list[dict], index: int) -> str:
    canonical = f"{SITE_URL}/writing/{post['route']}"
    title = f"{post['title']} | Munya Chipunza"
    description = article_description(post)
    intro = article_intro(post)

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_text(title)}</title>
    <meta name="description" content="{escape_attr(description)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{escape_attr(title)}">
    <meta property="og:description" content="{escape_attr(description)}">
    <meta property="og:site_name" content="Munya Chipunza">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{escape_attr(post['image_url'])}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape_attr(title)}">
    <meta name="twitter:description" content="{escape_attr(description)}">
    <meta name="twitter:image" content="{escape_attr(post['image_url'])}">
    <meta property="article:published_time" content="{post['published_date']}">
    <meta property="article:modified_time" content="{post['updated_date']}">
    <link rel="alternate" href="{SITE_URL}/blog-feed.xml" title="Munya Chipunza - RSS" type="application/rss+xml">
{ICON_LINKS}
    <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="/assets/css/style.css">
{GOOGLE_ANALYTICS_TAG}
  </head>
  <body>
{header("writing", "/writing", "All writing")}

    <main>
      <section class="article-hero">
        <a class="article-back" href="/writing">&larr; Back to all writing</a>
        <p class="post-tag">{escape_text(post["tag"])}</p>
        <h1>{escape_text(post["title"])}</h1>
        <p class="article-intro">{escape_text(intro)}</p>
        <div class="post-meta">
          <img src="/assets/images/munya-avatar.webp" alt="Munya Chipunza" width="256" height="256" decoding="async">
          <span>Munya Chipunza</span>
          <span>{format_date(post["published_date"])}</span>
          <span>{reading_time_label(post["minutes_to_read"])}</span>
        </div>
{render_audio_player(post)}
      </section>

      <article class="article-body">
        <div class="prose">
          {render_article_body(post)}
        </div>
      </article>

{render_engagement_section(post, canonical)}

{render_article_nav(posts, index)}

      <section class="form-section" id="contact">
        <div class="form-panel">
          <p class="eyebrow">Stay in touch</p>
          <h2>Send a note.</h2>
          <p>If this reflection met you where you are, you can respond here in plain words.</p>
{contact_form_fields(f"New message about {post['title']}", f"article: {post['route']}")}
        </div>
      </section>
    </main>

{FOOTER}

    <script src="/assets/js/site.js?v={ASSET_VERSION}"></script>
  </body>
</html>
"""


def render_redirect_page(destination: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Redirecting...</title>
    <link rel="canonical" href="{SITE_URL}{destination}">
    <meta http-equiv="refresh" content="0; url={destination}">
    <script>window.location.replace("{destination}");</script>
  </head>
  <body>
    <p>Redirecting to <a href="{destination}">{destination}</a>.</p>
  </body>
</html>
"""


def feed_html(post: dict) -> str:
    paragraphs = paragraph_text(post)
    return "".join(f"<p>{paragraph}</p>" for paragraph in paragraphs)


def render_feed(posts: list[dict]) -> str:
    items = []
    for post in posts:
        url = f"{SITE_URL}/writing/{post['route']}"
        pub_date = datetime.fromisoformat(post["published_date"].replace("Z", "+00:00")).strftime("%a, %d %b %Y %H:%M:%S GMT")
        items.append(
            f"""<item>
<title><![CDATA[{post["title"]}]]></title>
<description><![CDATA[{post["excerpt"]}]]></description>
<link>{url}</link>
<guid isPermaLink="true">{url}</guid>
<pubDate>{pub_date}</pubDate>
<content:encoded><![CDATA[{feed_html(post)}]]></content:encoded>
<dc:creator><![CDATA[Munya Chipunza]]></dc:creator>
</item>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
<channel>
<title><![CDATA[Munya Chipunza]]></title>
<description><![CDATA[Munya Chipunza]]></description>
<link>{SITE_URL}/writing</link>
<generator>Static site feed</generator>
<lastBuildDate>{datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>
<atom:link href="{SITE_URL}/blog-feed.xml" rel="self" type="application/rss+xml"/>
{''.join(items)}
</channel>
</rss>
"""


def render_sitemap(posts: list[dict], total_pages: int) -> str:
    urls = [
        (f"{SITE_URL}/", "daily"),
        (f"{SITE_URL}/about", "monthly"),
        (f"{SITE_URL}/writing", "weekly"),
        (f"{SITE_URL}/shop", "monthly"),
    ]
    for page_number in range(2, total_pages + 1):
        urls.append((f"{SITE_URL}/writing/page/{page_number}", "weekly"))
    for post in posts:
        urls.append((f"{SITE_URL}/writing/{post['route']}", "monthly"))

    url_xml = "\n".join(
        f"""  <url>
    <loc>{loc}</loc>
    <changefreq>{freq}</changefreq>
  </url>"""
        for loc, freq in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{url_xml}
</urlset>
"""


def render_shop_page() -> str:
    title = "Shop | MEN by Munya Chipunza"
    description = "MEN, Munya Chipunza's forthcoming book on biblical manhood, responsibility, formation, and steady strength. Launch details are coming soon."
    canonical = f"{SITE_URL}/shop"

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_text(title)}</title>
    <meta name="description" content="{escape_attr(description)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{escape_attr(title)}">
    <meta property="og:description" content="{escape_attr(description)}">
    <meta property="og:site_name" content="Munya Chipunza">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{SITE_URL}/assets/images/munya-home.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape_attr(title)}">
    <meta name="twitter:description" content="{escape_attr(description)}">
    <meta name="twitter:image" content="{SITE_URL}/assets/images/munya-home.jpg">
{ICON_LINKS}
    <link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" as="image" href="/assets/images/men-cover-portrait.jpg">
    <link rel="stylesheet" href="/assets/css/style.css">
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "Book",
        "name": "MEN",
        "alternateName": "Where are you? God's Question to Every Man",
        "author": {{
          "@type": "Person",
          "name": "Munya Chipunza",
          "url": "{SITE_URL}/"
        }},
        "url": "{canonical}",
        "description": "{escape_attr(description)}",
        "image": "{SITE_URL}/assets/images/munya-home.jpg"
      }}
    </script>
{GOOGLE_ANALYTICS_TAG}
  </head>
  <body>
{header("shop", "/writing", "Read a reflection")}

    <main class="page-wrap">
      <section class="shop-hero">
        <div class="shop-hero-copy">
          <p class="eyebrow">Book shop</p>
          <h1>MEN is coming soon.</h1>
          <p class="shop-lead">
            A book about biblical manhood, written for men who are trying to become steady without pretending they have everything figured out.
          </p>
          <div class="button-row">
            <a class="button button-primary" href="#launch-updates">Get launch updates</a>
            <a class="button button-secondary" href="/writing">Read the writing</a>
          </div>
        </div>
        <div class="shop-cover-stage book-jacket-stage will-reveal" aria-label="Full book jacket concept for MEN">
          <div class="book-jacket">
            <section class="jacket-panel jacket-front" aria-label="Front cover">
              <div class="jacket-edge jacket-edge-top"></div>
              <div class="jacket-front-copy">
                <span class="jacket-title">MEN</span>
                <span class="jacket-question">"Where are you?"</span>
                <span class="jacket-rule"></span>
                <span class="jacket-subtitle">God's Question to Every Man</span>
              </div>
              <img class="jacket-front-photo" src="/assets/images/men-cover-portrait.jpg" alt="" width="900" height="1140" decoding="async">
              <div class="jacket-photo-fade"></div>
              <div class="jacket-front-author">Munya Chipunza</div>
              <div class="jacket-edge jacket-edge-bottom"></div>
            </section>
            <aside class="jacket-spine" aria-label="Book spine">
              <span class="jacket-spine-title">MEN</span>
              <span class="jacket-spine-author">Munya Chipunza</span>
            </aside>
            <section class="jacket-panel jacket-back" aria-label="Back cover">
              <div class="jacket-back-copy">
                <p class="jacket-back-question">"Where are you?"</p>
                <span class="jacket-back-rule"></span>
                <p>God asked Adam this question in a garden thousands of years ago. He is still asking it today.</p>
                <p>Men are hiding. Behind performance. Behind silence. Behind titles, toughness, and the relentless pursuit of enough. The world has plenty of opinions about what a man should be &mdash; but few answers about what a man truly is.</p>
                <p>In <em>MEN</em>, Munya Chipunza goes back to the beginning &mdash; to God's original design for man, to where we lost it, and to the only One who can restore it. Not a book about trying harder. A book about coming home.</p>
                <p>From dust to glory. From hiding to wholeness.</p>
              </div>
              <div class="jacket-author-block">
                <img src="/assets/images/munya-avatar.webp" alt="" width="96" height="96" loading="lazy" decoding="async">
                <div>
                  <strong>Munya Chipunza</strong>
                  <span>munyachipunza.com</span>
                </div>
              </div>
              <div class="jacket-back-footer">
                <span>MUNYACHIPUNZA.COM</span>
                <div>
                  <div class="jacket-barcode" aria-hidden="true"></div>
                  <span class="jacket-isbn">ISBN 978-0-000-00000-0</span>
                </div>
              </div>
            </section>
          </div>
        </div>
      </section>

      <section class="shop-purchase-grid" aria-labelledby="purchase-status">
        <article class="shop-card shop-product-card will-reveal">
          <span class="shop-status-pill">Coming soon</span>
          <p class="eyebrow">Forthcoming book</p>
          <h2 id="purchase-status">MEN: "Where are you?"</h2>
          <p>
            This purchase page is being prepared now. No payment is being taken yet, and no preorder is active until the release details are final.
          </p>
          <dl class="product-details">
            <div>
              <dt>Status</dt>
              <dd>Writing and launch setup in progress</dd>
            </div>
            <div>
              <dt>Price</dt>
              <dd>To be announced</dd>
            </div>
            <div>
              <dt>Format</dt>
              <dd>Launch format to be confirmed</dd>
            </div>
            <div>
              <dt>Checkout</dt>
              <dd>Secure checkout will be added before sales open</dd>
            </div>
          </dl>
          <span class="button button-primary button-disabled" aria-disabled="true">Purchase coming soon</span>
        </article>

        <aside class="shop-card shop-notify-card will-reveal" id="launch-updates">
          <p class="eyebrow">Launch updates</p>
          <h2>Be first to know when the book is ready.</h2>
          <p>Join the list and I will send the release note, price, and buying link when the book is ready.</p>
          <div class="subscribe-form-shell">
{subscribe_form_fields("Book launch subscriber from munyachipunza.com", "book shop")}
          </div>
        </aside>
      </section>

      <section class="shop-info-grid" aria-labelledby="purchase-notes">
        <div class="shop-info-card will-reveal">
          <p class="eyebrow">What will be added</p>
          <h2 id="purchase-notes">The purchase flow will stay simple.</h2>
          <p>When the book is ready, this page will hold the live buying button, payment details, delivery expectations, and support contact in one place.</p>
        </div>
        <div class="shop-info-card will-reveal">
          <h3>Before launch</h3>
          <p>Use the update form if you want the announcement. The current button is intentionally disabled so nobody thinks they are buying today.</p>
        </div>
        <div class="shop-info-card will-reveal">
          <h3>At launch</h3>
          <p>The page will be updated with a secure checkout provider, final price, fulfilment details, and a short FAQ for buyers.</p>
        </div>
      </section>

{FORM_SECTION}
    </main>

{FOOTER}

    <script src="/assets/js/site.js?v={ASSET_VERSION}"></script>
  </body>
</html>
"""


def render_homepage_feature_grid(posts: list[dict]) -> str:
    lead_post = posts[0]
    side_posts = posts[1:3]
    main_excerpt = text_snippet(lead_post.get("summary") or lead_post["excerpt"] or first_paragraph_plain(lead_post), 165)

    side_cards = []
    for post in side_posts:
        side_cards.append(
            f"""            <a class="mini-card will-reveal" href="/writing/{post["route"]}">
              <span class="mini-tag">{escape_text(post["tag"])}</span>
              <h3 class="mini-title">{escape_text(post["title"])}</h3>
              <p>{escape_text(text_snippet(post.get("summary") or post["excerpt"] or first_paragraph_plain(post), 110))}</p>
              <div class="feature-meta">{format_date(post["published_date"])} &bull; {reading_time_label(post["minutes_to_read"])}</div>
            </a>"""
        )

    return f"""        <div class="feature-grid">
          <a class="feature-card will-reveal" href="/writing/{lead_post["route"]}">
            <span class="feature-tag">{escape_text(lead_post["tag"])}</span>
            <h3 class="feature-title">{escape_text(lead_post["title"])}</h3>
            <p class="feature-excerpt">
              {escape_text(main_excerpt)}
            </p>
            <div class="feature-meta">{format_date(lead_post["published_date"])} &bull; {reading_time_label(lead_post["minutes_to_read"])}</div>
          </a>

          <div class="feature-side">
{chr(10).join(side_cards)}
          </div>
        </div>"""


def update_homepage_sections(posts: list[dict]) -> None:
    home_path = ROOT / "index.html"
    home = home_path.read_text(encoding="utf-8")
    home = re.sub(
        r'        <div class="feature-grid">.*?        </div>\r?\n      </section>',
        f"{render_homepage_feature_grid(posts)}\n      </section>",
        home,
        count=1,
        flags=re.S,
    )
    home = re.sub(
        r'      <section class="subscribe-section">.*?      </section>',
        render_subscribe_section(
            "Get new reflections by email.",
            "If the writing helps, subscribe here and I will send the next reflection quietly when it is ready.",
            "homepage",
        ),
        home,
        count=1,
        flags=re.S,
    )
    home_path.write_text(home, encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def load_content_posts() -> list[dict]:
    if not CONTENT_POSTS_DIR.exists():
        return []

    posts: list[dict] = []
    required_fields = {"route", "title", "published_date", "updated_date", "paragraphs"}
    for path in sorted(CONTENT_POSTS_DIR.glob("*.json")):
        post = json.loads(path.read_text(encoding="utf-8"))
        missing = required_fields - set(post)
        if missing:
            raise ValueError(f"{path} is missing required field(s): {', '.join(sorted(missing))}")

        post.setdefault("old_slug", post["route"])
        post.setdefault("tag", "Reflection")
        post.setdefault("summary", first_paragraph_plain(post))
        post.setdefault("excerpt", post.get("summary") or first_paragraph_plain(post))
        post.setdefault("minutes_to_read", 2)
        post.setdefault("image_url", f"{SITE_URL}/assets/images/munya-home.jpg")
        posts.append(post)

    return posts


def main() -> None:
    # Legacy Wix posts have been migrated into LOCAL_POSTS, so the generator
    # no longer needs to call the Wix API. The fetch_access_token() and
    # fetch_posts() helpers are kept below as reference if a future re-import
    # from the legacy host is ever needed.
    posts = load_content_posts() + [dict(post) for post in LOCAL_POSTS]
    seen_routes: set[str] = set()
    duplicate_routes: set[str] = set()
    for post in posts:
        route = post["route"]
        if route in seen_routes:
            duplicate_routes.add(route)
        seen_routes.add(route)
    if duplicate_routes:
        raise ValueError(f"Duplicate post route(s): {', '.join(sorted(duplicate_routes))}")

    posts.sort(key=lambda post: post["published_date"], reverse=True)
    total_pages = (len(posts) + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE

    for page_number in range(1, total_pages + 1):
        start = (page_number - 1) * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        page_posts = posts[start:end]
        archive_html = render_archive_page(page_posts, page_number, total_pages, len(posts))
        if page_number == 1:
            write(ROOT / "writing" / "index.html", archive_html)
            write(ROOT / "blog" / "index.html", render_redirect_page("/writing"))
        else:
            write(ROOT / "writing" / "page" / str(page_number) / "index.html", archive_html)
            write(ROOT / "blog" / "page" / str(page_number) / "index.html", render_redirect_page(f"/writing/page/{page_number}"))

    for index, post in enumerate(posts):
        article_html = render_article_page(post, posts, index)
        write(ROOT / "writing" / f"{post['route']}.html", article_html)
        write(ROOT / "writing" / post["route"] / "index.html", article_html)
        write(ROOT / "blog" / post["route"] / "index.html", render_redirect_page(f"/writing/{post['route']}"))
        if post.get("old_slug"):
            write(ROOT / "post" / post["old_slug"] / "index.html", render_redirect_page(f"/writing/{post['route']}"))

    write(ROOT / "blog-feed.xml", render_feed(posts))
    write(ROOT / "sitemap.xml", render_sitemap(posts, total_pages))
    write(ROOT / "shop" / "index.html", render_shop_page())
    write(ROOT / "shop.html", render_shop_page())
    update_homepage_sections(posts)


if __name__ == "__main__":
    main()
