import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('Starting exact data seeding based on specification...');
  
  // Clean up existing data to prevent duplicates on re-seed
  await prisma.pageView.deleteMany();
  await prisma.translation.deleteMany();
  await prisma.video.deleteMany();
  await prisma.localSlang.deleteMany();
  await prisma.cultureShock.deleteMany();
  await prisma.country.deleteMany();

  // ======================================
  // 1. COLOMBIA (CO)
  // ======================================
  const colombia = await prisma.country.create({
    data: {
      name: 'Colombia',
      code: 'CO',
      flag_emoji: '🇨🇴',
      latitude: 4.5709,
      longitude: -74.2973,
      primary_color: '#FCD116',
      cultureShocks: {
        create: [
          {
            title: 'Time is Flexible (Hora Latina)',
            description: 'Don\'t be surprised if meetings start 15-30 minutes late. Colombians have a very relaxed approach to time compared to North American or European cultures.',
            icon: '⏰',
            image_url: '/images/colombia/time.jpg',
            display_order: 1
          },
          {
            title: 'The Pointing Lip',
            description: 'Instead of pointing with their fingers, Colombians often point with their lips/chin. It might look like they are puckering up for a kiss.',
            icon: '👄',
            image_url: '/images/colombia/lips.jpg',
            display_order: 2
          },
          {
            title: 'Cheese in Hot Chocolate',
            description: 'A traditional breakfast or evening snack involves dropping chunks of salty cheese into sweet hot chocolate. It melts into a delicious, gooey treat.',
            icon: '☕',
            image_url: '/images/colombia/chocolate.jpg',
            display_order: 3
          },
          {
            title: 'Extreme Politeness',
            description: 'Colombians are incredibly polite. You will constantly hear "a la orden" (at your service), and asking for a favor usually involves a long, polite prelude.',
            icon: '🙏',
            image_url: '/images/colombia/polite.jpg',
            display_order: 4
          },
          {
            title: 'No Shorts in the City',
            description: 'In cities like Bogotá or Medellín, adults rarely wear shorts unless they are doing sports, regardless of the temperature. Long pants are standard.',
            icon: '👖',
            image_url: '/images/colombia/pants.jpg',
            display_order: 5
          }
        ]
      },
      slangs: {
        create: [
          { term: '¡Qué pena!', meaning: 'Sorry! / Excuse me', context: 'Used constantly for everything, not just embarrassment.', category: 'expression', display_order: 1, pronunciation: 'keh PEH-nah' },
          { term: 'Chimba', meaning: 'Cool / Awesome', context: 'Can be used for almost anything good. "¡Qué chimba!"', category: 'expression', display_order: 2, pronunciation: 'CHEEM-bah' },
          { term: 'Parce / Parcero', meaning: 'Friend / Bro', context: 'The most common way to address a friend.', category: 'greeting', display_order: 3, pronunciation: 'PAR-seh' },
          { term: 'Bacano', meaning: 'Cool / Nice', context: 'Similar to chimba, but slightly more polite/standard.', category: 'expression', display_order: 4, pronunciation: 'bah-KAH-no' },
          { term: 'Tinto', meaning: 'Black Coffee', context: 'A small cup of black coffee, often sweetened.', category: 'food', display_order: 5, pronunciation: 'TEEN-toh' },
          { term: 'Dar papaya', meaning: 'To ask for trouble / To make yourself vulnerable', context: 'The #1 rule in Colombia: No des papaya (Don\'t make yourself an easy target).', category: 'expression', display_order: 6 },
          { term: 'Guayabo', meaning: 'Hangover', context: 'Used after a long night of drinking Aguardiente.', category: 'other', display_order: 7 },
          { term: 'Paila', meaning: 'Too bad / Screwed', context: '"Ya es tarde, paila." (It\'s late, too bad).', category: 'expression', display_order: 8 },
          { term: 'Rumbear', meaning: 'To party', context: 'Colombians love to rumbear.', category: 'expression', display_order: 9 },
          { term: 'Pola', meaning: 'Beer', context: 'Named after a famous historical figure, but universally means beer now.', category: 'food', display_order: 10 },
          { term: 'Quiubo', meaning: 'What\'s up?', context: 'Short for "Qué hubo" (What happened).', category: 'greeting', display_order: 11 },
          { term: 'Marica', meaning: 'Dude / Bro', context: 'Literally means something offensive, but used affectionately among friends.', category: 'greeting', display_order: 12 },
          { term: 'Plata', meaning: 'Money', context: 'Silver. Used universally for money.', category: 'other', display_order: 13 },
          { term: 'Mamar gallo', meaning: 'To joke around / To pull someone\'s leg', context: 'Literally means "to suck rooster", but means joking.', category: 'expression', display_order: 14 },
          { term: 'Camello', meaning: 'Work / Job', context: 'Literally "camel", used because work is hard.', category: 'other', display_order: 15 },
          { term: 'Cantaleta', meaning: 'Nagging', context: 'Usually used when mothers are scolding their kids repeatedly.', category: 'expression', display_order: 16 },
          { term: 'Fartusco', meaning: 'Ugly / Unpleasant', context: 'Not very common everywhere, but used in some regions.', category: 'insult', display_order: 17 },
          { term: 'Sisas', meaning: 'Yes', context: 'Very informal affirmative.', category: 'expression', display_order: 18 },
          { term: 'Ñero', meaning: 'Street person / Thug', context: 'Used descriptively or as a mild insult.', category: 'insult', display_order: 19 },
          { term: 'A la orden', meaning: 'At your service', context: 'Used constantly by shopkeepers, waiters, etc.', category: 'greeting', display_order: 20 }
        ]
      },
      videos: {
        create: [
          { title: '10 Culture Shocks in Colombia', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '08:32', display_order: 1 },
          { title: 'Colombian Spanish Slang Guide', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '12:15', display_order: 2 },
          { title: 'What not to do in Colombia', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '15:20', display_order: 3 }
        ]
      }
    }
  });

  // ======================================
  // 2. USA (US)
  // ======================================
  const usa = await prisma.country.create({
    data: {
      name: 'United States',
      code: 'US',
      flag_emoji: '🇺🇸',
      latitude: 37.0902,
      longitude: -95.7129,
      primary_color: '#3C3B6E',
      cultureShocks: {
        create: [
          { title: 'Superficial Friendliness', description: 'Americans are friendly but it doesn\'t mean deep friendship. "Let\'s hang out sometime!" often means nothing.', icon: '🙂', image_url: '/images/usa/friendly.jpg', display_order: 1 },
          { title: 'Tipping is Mandatory', description: '15-20% tip is expected in restaurants. Servers rely on tips for income. Not tipping is extremely rude.', icon: '💰', image_url: '/images/usa/tip.jpg', display_order: 2 },
          { title: 'Car-Dependent Culture', description: 'Public transport is limited outside major cities. You NEED a car for most places. Distances are huge.', icon: '🚗', image_url: '/images/usa/car.jpg', display_order: 3 },
          { title: 'Small Talk is Essential', description: '"How are you?" is a greeting, not a real question. Expected answer: "Good, you?" Keep it brief.', icon: '📱', image_url: '/images/usa/smalltalk.jpg', display_order: 4 },
          { title: 'Lawsuit Culture', description: 'Americans sue frequently. Warning labels everywhere. People are cautious about liability.', icon: '⚖️', image_url: '/images/usa/lawsuit.jpg', display_order: 5 }
        ]
      },
      slangs: {
        create: [
          { term: "Y'all", meaning: "You all", context: "Southern US, used universally to address multiple people.", category: "greeting", display_order: 1 },
          { term: "Gonna", meaning: "Going to", context: "Universal informal future tense.", category: "expression", display_order: 2 },
          { term: "Wanna", meaning: "Want to", context: "Universal informal expression of desire.", category: "expression", display_order: 3 },
          { term: "Ain't", meaning: "Am not / Is not / Are not", context: "Informal negation.", category: "expression", display_order: 4 },
          { term: "Dude", meaning: "Guy / Person", context: "Casual address for anyone.", category: "greeting", display_order: 5 },
          { term: "Bucks", meaning: "Dollars", context: "Used when referring to money.", category: "other", display_order: 6 },
          { term: "Knock it off", meaning: "Stop it", context: "A firm command to stop doing something annoying.", category: "expression", display_order: 7 },
          { term: "Screw up", meaning: "Make a mistake", context: "Used when someone ruins a task.", category: "expression", display_order: 8 },
          { term: "Hang out", meaning: "Spend time together", context: "Casual social interaction.", category: "expression", display_order: 9 },
          { term: "Hit the road", meaning: "Start traveling / Leave", context: "Time to go.", category: "expression", display_order: 10 },
          { term: "Piece of cake", meaning: "Very easy", context: "Used to describe a simple task.", category: "expression", display_order: 11 },
          { term: "Break a leg", meaning: "Good luck", context: "Originally from theater, means good luck.", category: "expression", display_order: 12 },
          { term: "Bet", meaning: "Okay / Agreement", context: "Gen Z slang for agreement.", category: "expression", display_order: 13 },
          { term: "No cap", meaning: "No lie / For real", context: "Gen Z slang meaning telling the truth.", category: "expression", display_order: 14 },
          { term: "Salty", meaning: "Bitter / Angry", context: "Being needlessly upset.", category: "insult", display_order: 15 },
          { term: "Sick / Fire", meaning: "Awesome / Cool", context: "Youth slang for something amazing.", category: "expression", display_order: 16 },
          { term: "Lowkey", meaning: "Somewhat / Kind of", context: "Doing something secretly or slightly.", category: "expression", display_order: 17 },
          { term: "Highkey", meaning: "Very / Really", context: "Openly or strongly.", category: "expression", display_order: 18 },
          { term: "Ghosted", meaning: "Ignored completely", context: "When someone cuts off all communication.", category: "expression", display_order: 19 },
          { term: "Sus", meaning: "Suspicious", context: "From the game Among Us, means acting sketchy.", category: "expression", display_order: 20 }
        ]
      },
      videos: {
        create: [
          { title: 'Understanding US Tipping Culture', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '05:40', display_order: 1 },
          { title: 'Small Talk in America', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '10:05', display_order: 2 },
          { title: 'The Ultimate Guide to US Slang', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '14:22', display_order: 3 }
        ]
      }
    }
  });

  // ======================================
  // 3. BRAZIL (BR)
  // ======================================
  const brazil = await prisma.country.create({
    data: {
      name: 'Brazil',
      code: 'BR',
      flag_emoji: '🇧🇷',
      latitude: -14.2350,
      longitude: -51.9253,
      primary_color: '#009b3a',
      cultureShocks: {
        create: [
          { title: 'Flexible Time (Brazilian Time)', description: 'Similar to Colombia. Events start late. "Now" can mean in 2 hours.', icon: '⏰', image_url: '/images/brazil/time.jpg', display_order: 1 },
          { title: 'Physical Affection is Normal', description: 'Brazilians are VERY touchy. Hugs, cheek kisses (2-3), arm touching during conversation.', icon: '🤗', image_url: '/images/brazil/affection.jpg', display_order: 2 },
          { title: 'Music Everywhere', description: 'Brazilians blast music publicly - on buses, beaches, streets. It\'s not considered rude.', icon: '🎵', image_url: '/images/brazil/music.jpg', display_order: 3 },
          { title: 'Carnival is Serious Business', description: 'The whole country shuts down for Carnival. It\'s THE most important cultural event.', icon: '💃', image_url: '/images/brazil/carnival.jpg', display_order: 4 },
          { title: 'Beach Culture Dominance', description: 'Beach is lifestyle, not just recreation. Tiny swimwear is normal. Body positivity is high.', icon: '🏖️', image_url: '/images/brazil/beach.jpg', display_order: 5 }
        ]
      },
      slangs: {
        create: [
          { term: 'Valeu', meaning: 'Thanks / Cool', context: 'Casual way to say thank you or goodbye.', category: 'expression', display_order: 1 },
          { term: 'Beleza?', meaning: 'What\'s up?', context: 'Literally means "beauty", used as a casual greeting.', category: 'greeting', display_order: 2 },
          { term: 'Tá ligado?', meaning: 'You know? / Understand?', context: 'Used at the end of sentences.', category: 'expression', display_order: 3 },
          { term: 'Cara / Mano', meaning: 'Dude / Guy', context: 'Very common fillers when talking to males.', category: 'greeting', display_order: 4 },
          { term: 'Massa', meaning: 'Cool / Awesome', context: 'Used to describe something great.', category: 'expression', display_order: 5 },
          { term: 'Legal', meaning: 'Cool / Nice', context: 'The standard and most common word for cool.', category: 'expression', display_order: 6 },
          { term: 'Bala', meaning: 'Candy (or bullet)', context: 'Usually candy, but context matters!', category: 'food', display_order: 7 },
          { term: 'Gato / Gata', meaning: 'Hot guy / girl', context: 'Literally means cat, used for attractive people.', category: 'other', display_order: 8 },
          { term: 'Pão de queijo', meaning: 'Cheese bread', context: 'A cultural staple food.', category: 'food', display_order: 9 },
          { term: 'Caipirinha', meaning: 'National cocktail', context: 'Cachaça, sugar, and lime.', category: 'food', display_order: 10 },
          { term: 'Brigadeiro', meaning: 'Chocolate sweet', context: 'The most popular party dessert.', category: 'food', display_order: 11 },
          { term: 'Saudade', meaning: 'Deep longing / nostalgia', context: 'An untranslatable deep feeling of missing someone/something.', category: 'expression', display_order: 12 },
          { term: 'Jeitinho', meaning: 'Brazilian way of bending rules', context: 'Using charm or connections to bypass bureaucracy.', category: 'expression', display_order: 13 },
          { term: 'Gringo', meaning: 'Foreigner', context: 'Unlike in Spanish America, this holds no inherently negative weight in Brazil.', category: 'other', display_order: 14 },
          { term: 'Cerveja', meaning: 'Beer', context: 'Served extremely cold.', category: 'food', display_order: 15 },
          { term: 'Futebol', meaning: 'Soccer/Football', context: 'It is a religion in Brazil.', category: 'other', display_order: 16 },
          { term: 'Carioca', meaning: 'Person from Rio', context: 'Demonym for Rio de Janeiro locals.', category: 'other', display_order: 17 },
          { term: 'Paulista', meaning: 'Person from São Paulo', context: 'Demonym for São Paulo locals.', category: 'other', display_order: 18 },
          { term: 'Favelado', meaning: 'Person from favela', context: 'Can be descriptive or derogatory.', category: 'other', display_order: 19 },
          { term: 'Irmão / Mano', meaning: 'Brother / Bro', context: 'Used affectionately for close friends.', category: 'greeting', display_order: 20 }
        ]
      },
      videos: {
        create: [
          { title: 'The Brazilian Jeitinho', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '06:12', display_order: 1 },
          { title: 'Carnival Explained', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '08:45', display_order: 2 },
          { title: 'Brazilian Portuguese vs Portugal', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '11:10', display_order: 3 }
        ]
      }
    }
  });

  // ======================================
  // 4. FRANCE (FR)
  // ======================================
  const france = await prisma.country.create({
    data: {
      name: 'France',
      code: 'FR',
      flag_emoji: '🇫🇷',
      latitude: 46.2276,
      longitude: 2.2137,
      primary_color: '#0055A4',
      cultureShocks: {
        create: [
          { title: 'Formal Greetings are Mandatory', description: 'Always say "Bonjour" when entering shops/elevators. Not greeting is VERY rude.', icon: '🥖', image_url: '/images/france/bonjour.jpg', display_order: 1 },
          { title: 'Lunch is Sacred', description: '2-hour lunch breaks are normal. Eating at your desk is frowned upon. Food is culture, not fuel.', icon: '🍷', image_url: '/images/france/lunch.jpg', display_order: 2 },
          { title: 'Customer is NOT Always Right', description: 'French service can seem rude. Staff won\'t smile automatically. Efficiency over friendliness.', icon: '🚫', image_url: '/images/france/service.jpg', display_order: 3 },
          { title: 'Direct Communication Style', description: 'French people debate passionately. Disagreement is intellectual, not personal. Expect bluntness.', icon: '💬', image_url: '/images/france/debate.jpg', display_order: 4 },
          { title: 'Smoking is Still Common', description: 'Despite bans, terraces are full of smokers. Smoke tolerance is much higher than US/Canada.', icon: '🚭', image_url: '/images/france/smoke.jpg', display_order: 5 }
        ]
      },
      slangs: {
        create: [
          { term: 'Bonjour', meaning: 'Hello', context: 'ALWAYS say this to shopkeepers!', category: 'greeting', display_order: 1 },
          { term: 'Bonsoir', meaning: 'Good evening', context: 'Hello but after 5-6 PM.', category: 'greeting', display_order: 2 },
          { term: 'Ça va?', meaning: 'How are you?', context: 'Very common casual greeting.', category: 'greeting', display_order: 3 },
          { term: 'Merci', meaning: 'Thank you', context: 'Basic politeness.', category: 'expression', display_order: 4 },
          { term: 'S\'il vous plaît', meaning: 'Please (formal)', context: 'Use this with strangers.', category: 'expression', display_order: 5 },
          { term: 'Bisous', meaning: 'Kisses', context: 'Used at the end of texts or emails to friends.', category: 'expression', display_order: 6 },
          { term: 'Bof', meaning: 'Meh / Whatever', context: 'A very French shrug.', category: 'expression', display_order: 7 },
          { term: 'C\'est nul', meaning: 'That sucks', context: 'When something is bad or uninteresting.', category: 'expression', display_order: 8 },
          { term: 'Mec / Meuf', meaning: 'Guy / Girl', context: 'Very common slang for people.', category: 'other', display_order: 9 },
          { term: 'Ouf', meaning: 'Crazy', context: 'Verlan (reversed slang) for fou.', category: 'expression', display_order: 10 },
          { term: 'Chelou', meaning: 'Weird', context: 'Verlan for louche.', category: 'expression', display_order: 11 },
          { term: 'Kiffer', meaning: 'To like / love', context: 'Slang borrowed from Arabic.', category: 'expression', display_order: 12 },
          { term: 'Bouffer', meaning: 'To eat', context: 'Casual slang for eating.', category: 'food', display_order: 13 },
          { term: 'Boulot', meaning: 'Work / Job', context: 'Casual term for a job.', category: 'other', display_order: 14 },
          { term: 'Fric', meaning: 'Money', context: 'Slang for cash.', category: 'other', display_order: 15 },
          { term: 'Sympa', meaning: 'Nice / Cool', context: 'Short for sympathique.', category: 'expression', display_order: 16 },
          { term: 'Désolé(e)', meaning: 'Sorry', context: 'Apology.', category: 'expression', display_order: 17 },
          { term: 'Bonne journée', meaning: 'Have a good day', context: 'Said upon leaving a shop or encounter.', category: 'greeting', display_order: 18 },
          { term: 'À bientôt', meaning: 'See you soon', context: 'Standard departure phrase.', category: 'greeting', display_order: 19 },
          { term: 'Putain', meaning: 'Damn / F***', context: 'Extremely common filler swear word.', category: 'insult', display_order: 20 }
        ]
      },
      videos: {
        create: [
          { title: 'The Art of the Bise (French Kiss Greeting)', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '04:15', display_order: 1 },
          { title: 'Why French Waiters Aren\'t Rude', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '09:20', display_order: 2 },
          { title: 'Surviving a French Dinner Party', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '11:45', display_order: 3 }
        ]
      }
    }
  });

  // ======================================
  // 5. GERMANY (DE)
  // ======================================
  const germany = await prisma.country.create({
    data: {
      name: 'Germany',
      code: 'DE',
      flag_emoji: '🇩🇪',
      latitude: 51.1657,
      longitude: 10.4515,
      primary_color: '#FFCE00',
      cultureShocks: {
        create: [
          { title: 'Punctuality is SACRED', description: 'Being late is extremely disrespectful. Arrive 5-10 min early. Germans value time precision.', icon: '⏰', image_url: '/images/germany/time.jpg', display_order: 1 },
          { title: 'Rules are Absolute', description: 'Jaywalking is illegal and judged. Follow ALL rules. Rules create order and trust.', icon: '🚦', image_url: '/images/germany/rules.jpg', display_order: 2 },
          { title: 'Privacy is Highly Valued', description: 'Germans don\'t small talk. Direct questions about income/religion are invasive. Boundaries are firm.', icon: '🚪', image_url: '/images/germany/privacy.jpg', display_order: 3 },
          { title: 'Recycling is Complex', description: '5+ different bins. Sorting is mandatory. Neighbors will judge improper recycling.', icon: '♻️', image_url: '/images/germany/recycle.jpg', display_order: 4 },
          { title: 'Work-Life Balance is Enforced', description: 'Sundays are rest days. Most stores closed. No work emails after hours. Vacation is sacred.', icon: '💼', image_url: '/images/germany/work.jpg', display_order: 5 }
        ]
      },
      slangs: {
        create: [
          { term: 'Guten Tag', meaning: 'Hello (formal)', context: 'Classic and proper German greeting.', category: 'greeting', display_order: 1 },
          { term: 'Tschüss', meaning: 'Bye (casual)', context: 'Informal way to say goodbye.', category: 'greeting', display_order: 2 },
          { term: 'Prost!', meaning: 'Cheers!', context: 'Used with beer. Make eye contact!', category: 'expression', display_order: 3 },
          { term: 'Bitte', meaning: 'Please / You\'re welcome', context: 'A very versatile word.', category: 'expression', display_order: 4 },
          { term: 'Danke', meaning: 'Thank you', context: 'Standard thanks.', category: 'expression', display_order: 5 },
          { term: 'Entschuldigung', meaning: 'Excuse me / Sorry', context: 'A long word you must learn.', category: 'expression', display_order: 6 },
          { term: 'Krass', meaning: 'Crazy / Intense', context: 'Can be positive or negative.', category: 'expression', display_order: 7 },
          { term: 'Geil', meaning: 'Awesome / Cool', context: 'Literally means horny, but universally means cool.', category: 'expression', display_order: 8 },
          { term: 'Alter', meaning: 'Dude', context: 'Literally means age/old.', category: 'greeting', display_order: 9 },
          { term: 'Quatsch', meaning: 'Nonsense / Rubbish', context: 'When someone says something untrue.', category: 'expression', display_order: 10 },
          { term: 'Schade', meaning: 'Too bad / Pity', context: 'Expressing slight disappointment.', category: 'expression', display_order: 11 },
          { term: 'Moin', meaning: 'Hi', context: 'Used in Northern Germany at any time of day.', category: 'greeting', display_order: 12 },
          { term: 'Nee', meaning: 'No (casual)', context: 'Casual version of Nein.', category: 'expression', display_order: 13 },
          { term: 'Ja', meaning: 'Yes', context: 'Standard affirmative.', category: 'expression', display_order: 14 },
          { term: 'Genau', meaning: 'Exactly', context: 'Used constantly in agreement during conversation.', category: 'expression', display_order: 15 },
          { term: 'Feierabend', meaning: 'End of workday', context: 'A cultural concept honoring post-work rest.', category: 'other', display_order: 16 },
          { term: 'Gemütlich', meaning: 'Cozy / Comfortable', context: 'Untranslatable feeling of warmth and comfort.', category: 'expression', display_order: 17 },
          { term: 'Schadenfreude', meaning: 'Joy from others\' misfortune', context: 'Another famous untranslatable word.', category: 'expression', display_order: 18 },
          { term: 'Weltschmerz', meaning: 'World-weariness', context: 'Feeling the pain of the whole world.', category: 'expression', display_order: 19 },
          { term: 'Fernweh', meaning: 'Wanderlust', context: 'An ache for distant places.', category: 'expression', display_order: 20 }
        ]
      },
      videos: {
        create: [
          { title: 'The German Stare Explained', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '05:30', display_order: 1 },
          { title: 'Why Rules Matter in Germany', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '12:05', display_order: 2 },
          { title: 'German Recycling System Guide', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '08:42', display_order: 3 }
        ]
      }
    }
  });

  // ======================================
  // 6. CHINA (CN)
  // ======================================
  const china = await prisma.country.create({
    data: {
      name: 'China',
      code: 'CN',
      flag_emoji: '🇨🇳',
      latitude: 35.8617,
      longitude: 104.1954,
      primary_color: '#EE1C25',
      cultureShocks: {
        create: [
          { title: 'Rice with EVERYTHING', description: 'Rice accompanies most meals. Eating rice shows you\'re truly eating. No rice = not a real meal.', icon: '🍚', image_url: '/images/china/rice.jpg', display_order: 1 },
          { title: 'Bargaining is Expected', description: 'Prices are negotiable in markets. Not bargaining means you\'re rich/stupid. It\'s a game.', icon: '💰', image_url: '/images/china/bargain.jpg', display_order: 2 },
          { title: 'Cash is Dead', description: 'WeChat Pay/Alipay everywhere. Even street vendors don\'t accept cash. Digital payment is mandatory.', icon: '📱', image_url: '/images/china/pay.jpg', display_order: 3 },
          { title: 'Saying \'No\' Directly is Rude', description: 'Chinese people avoid direct refusal. "Maybe" or "difficult" usually means no.', icon: '🙅', image_url: '/images/china/no.jpg', display_order: 4 },
          { title: 'Gift Giving has Rules', description: 'Never give clocks (death symbol), open gifts privately, refuse 3 times before accepting (politeness ritual).', icon: '🎁', image_url: '/images/china/gift.jpg', display_order: 5 }
        ]
      },
      slangs: {
        create: [
          { term: '你好 (Nǐ hǎo)', meaning: 'Hello', context: 'Standard greeting.', category: 'greeting', display_order: 1 },
          { term: '谢谢 (Xièxiè)', meaning: 'Thank you', context: 'Standard thanks.', category: 'expression', display_order: 2 },
          { term: '不客气 (Bù kèqì)', meaning: 'You\'re welcome', context: 'Polite response.', category: 'expression', display_order: 3 },
          { term: '对不起 (Duìbùqǐ)', meaning: 'Sorry', context: 'When you make a mistake.', category: 'expression', display_order: 4 },
          { term: '没关系 (Méi guānxi)', meaning: 'No problem', context: 'Response to an apology.', category: 'expression', display_order: 5 },
          { term: '加油 (Jiāyóu)', meaning: 'Go for it! / Good luck!', context: 'Literally "add oil", used to encourage.', category: 'expression', display_order: 6 },
          { term: '厉害 (Lìhài)', meaning: 'Awesome / Impressive', context: 'Praising someone\'s skills.', category: 'expression', display_order: 7 },
          { term: '牛 (Niú)', meaning: 'Cool / Badass', context: 'Literally means cow.', category: 'expression', display_order: 8 },
          { term: '土豪 (Tǔháo)', meaning: 'Nouveau riche', context: 'Internet slang for new money.', category: 'insult', display_order: 9 },
          { term: '吃货 (Chīhuò)', meaning: 'Foodie', context: 'Literally "eating goods".', category: 'food', display_order: 10 },
          { term: '白富美 (Bái fù měi)', meaning: 'Ideal woman', context: 'Fair, rich, beautiful.', category: 'other', display_order: 11 },
          { term: '高富帅 (Gāo fù shuài)', meaning: 'Ideal man', context: 'Tall, rich, handsome.', category: 'other', display_order: 12 },
          { term: '给力 (Gěi lì)', meaning: 'Awesome / Powerful', context: 'Internet slang.', category: 'expression', display_order: 13 },
          { term: '靠谱 (Kàopǔ)', meaning: 'Reliable', context: 'Trustworthy person or plan.', category: 'expression', display_order: 14 },
          { term: '坑爹 (Kēng diē)', meaning: 'Rip-off', context: 'Disappointing or a scam.', category: 'expression', display_order: 15 },
          { term: '萌 (Méng)', meaning: 'Cute', context: 'Anime-style cuteness.', category: 'expression', display_order: 16 },
          { term: '呵呵 (Hēhē)', meaning: 'Haha (sarcastic)', context: 'Dismissive or sarcastic online laugh.', category: 'expression', display_order: 17 },
          { term: '666 (Liù liù liù)', meaning: 'Skilled / Pro', context: 'Gamer slang for playing well.', category: 'expression', display_order: 18 },
          { term: '88 (Bā bā)', meaning: 'Bye bye', context: 'Sounds like bye.', category: 'greeting', display_order: 19 },
          { term: '520 (Wǔ èr líng)', meaning: 'I love you', context: 'Sounds similar in Mandarin.', category: 'expression', display_order: 20 }
        ]
      },
      videos: {
        create: [
          { title: 'The Concept of "Face" (Mianzi)', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '08:15', display_order: 1 },
          { title: 'WeChat and Digital Life in China', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '14:20', display_order: 2 },
          { title: 'Chinese Business Etiquette', video_type: 'youtube', video_url: 'https://youtube.com/embed/dQw4w9WgXcQ', duration: '10:45', display_order: 3 }
        ]
      }
    }
  });

  console.log('Seeding completed successfully!');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
