import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from '../../../src/pages/index.module.css';
import chapterStyles from '../../../src/pages/chapters.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/introduction-to-physical-ai/chapter">
            کتاب پڑھیں
          </Link>
        </div>
      </div>
    </header>
  );
}

// Chapter data in Urdu
const chapters = [
  {
    id: 1,
    number: 'باب 1',
    title: 'جسمانی مصنوعی ذہانت کا تعارف',
    description: 'روبوٹکس میں جسمانی مصنوعی ذہانت کے بنیادیات کو سمجھنا۔ جسمانی شعور، حسی-حرکتی یکجہتی، اور جسمانی ماحول میں حقیقی وقت کی پروسیسنگ کے بارے میں سیکھیں۔',
    path: '/docs/introduction-to-physical-ai/chapter'
  },
  {
    id: 2,
    number: 'باب 2',
    title: 'روبوٹکس کی بنیادیں - نظام، ساخت اور بنیادی میکانزم',
    description: 'روبوٹکس میں بنیادی نظام، ساخت، اور میکانزم کو سمجھنا۔ بنیادی اجزاء، کنیمیٹکس، ڈائینیمکس، اور مختلف روبوٹک آرکیٹیکچر کی تفصیل دیکھیں۔',
    path: '/docs/foundations-of-robotics/chapter'
  },
  {
    id: 3,
    number: 'باب 3',
    title: 'انسان متاثرہ ڈیزائن کے اصول انسان نما روبوٹکس میں',
    description: 'اس کا جائزہ لینا کہ حیاتیاتی نظام انسان نما روبوٹک ڈیزائن کو کیسے متاثر کرتا ہے۔ حیاتیاتی نقل، انسان متاثرہ ذہنی نظام، اور انسان متاثرہ ڈیزائن میں چیلنجز کے بارے میں سیکھیں۔',
    path: '/docs/human-inspired-design/chapter'
  },
  {
    id: 4,
    number: 'باب 4',
    title: 'ادراک کے نظام',
    description: 'ان حسی نظام کو تلاش کریں جو روبوٹس کو اپنے ماحول کو سمجھنے کے قابل بناتے ہیں۔ کمپیوٹر بینائش، حسی فیوژن، اور روبوٹکس اطلاقیات کے لیے حقیقی وقت کی ادراک الگورتھم کے بارے میں سیکھیں۔',
    path: '/docs/perception-systems/chapter'
  },
  {
    id: 5,
    number: 'باب 5',
    title: 'مصنوعی ذہانت اور گہری سیکھ',
    description: 'روبوٹکس میں مصنوعی ذہانت اور گہری سیکھ کے کردار کو سمجھنا۔ نیورل نیٹ ورکس، مضبوطی سیکھ، اور روبوٹک نظام میں ان کی اطلاقیات کی تفصیل دیکھیں۔',
    path: '/docs/ai-deep-learning/chapter'
  },
  {
    id: 6,
    number: 'باب 6',
    title: 'انسان نما حرکت',
    description: 'انسان نما روبوٹس میں حرکت اور نقل کے اصولوں کا مطالعہ کریں۔ دو پاؤں والی چال، توازن کنٹرول، اور انسان نما روبوٹک نظام کے لیے متحرک حرکت منصوبہ بندی کے بارے میں سیکھیں۔',
    path: '/docs/humanoid-locomotion/chapter'
  }
];

function ChapterCards() {
  return (
    <section className={chapterStyles.chapterCardsContainer}>
      <div className={chapterStyles.chapterCardsGrid}>
        {chapters.map((chapter) => (
          <div key={chapter.id} className={chapterStyles.chapterCard}>
            <div className={chapterStyles.chapterCardHeader}>
              <span className={chapterStyles.chapterCardNumber}>{chapter.number}</span>
              <h3 className={chapterStyles.chapterCardTitle}>{chapter.title}</h3>
            </div>
            <div className={chapterStyles.chapterCardBody}>
              <p className={chapterStyles.chapterCardDescription}>{chapter.description}</p>
              <div className={chapterStyles.chapterCardFooter}>
                <Link to={chapter.path} className={chapterStyles.chapterCardLink}>
                  باب پڑھیں
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={` ${siteConfig.title} سے سلام`}
      description="AI- native کتاب مع RAG چیٹ بوٹ">
      <HomepageHeader />
      <main>
        <ChapterCards />
        <section className={`${styles.features} ${chapterStyles.featuresSection}`}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <h2>جسمانی مصنوعی ذہانت</h2>
                <p>روبوٹکس میں جسمانی مصنوعی ذہانت کے بنیادیات کو سمجھنا۔</p>
              </div>
              <div className="col col--4">
                <h2>تعاملی سیکھنا</h2>
                <p>سوالات پوچھیں اور کتاب کے مواد سے متاثرہ AI اسسٹنٹ سے جوابات حاصل کریں۔</p>
              </div>
              <div className="col col--4">
                <h2>انسان نما روبوٹکس</h2>
                <p>روبوٹکس نظام میں انسان متاثرہ ڈیزائن کے اصولوں کو تلاش کریں۔</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}