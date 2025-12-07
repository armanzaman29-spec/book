import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';
import chapterStyles from './chapters.module.css';

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
            Read the Textbook
          </Link>
        </div>
      </div>
    </header>
  );
}

// Chapter data
const chapters = [
  {
    id: 1,
    number: 'Chapter 1',
    title: 'Introduction to Physical AI',
    description: 'Understanding the fundamentals of Physical AI and its applications in robotics. Learn about embodied cognition, sensorimotor integration, and real-time processing in physical environments.',
    path: '/docs/introduction-to-physical-ai/chapter'
  },
  {
    id: 2,
    number: 'Chapter 2',
    title: 'Foundations of Robotics - Systems, Structure & Core Mechanisms',
    description: 'Understanding the fundamental systems, structures, and mechanisms in robotics. Explore core components, kinematics, dynamics, and different robotic architectures.',
    path: '/docs/foundations-of-robotics/chapter'
  },
  {
    id: 3,
    number: 'Chapter 3',
    title: 'Human-Inspired Design Principles in Humanoid Robotics',
    description: 'Exploring how biological systems inspire humanoid robotic design. Learn about biomimicry, human-inspired cognitive systems, and challenges in human-inspired design.',
    path: '/docs/human-inspired-design/chapter'
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
                  Read Chapter
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
      title={`Hello from ${siteConfig.title}`}
      description="AI-Native Textbook with RAG Chatbot">
      <HomepageHeader />
      <main>
        <ChapterCards />
        <section className={`${styles.features} ${chapterStyles.featuresSection}`}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <h2>Physical AI</h2>
                <p>Understanding the fundamentals of Physical AI and its applications in robotics.</p>
              </div>
              <div className="col col--4">
                <h2>Interactive Learning</h2>
                <p>Ask questions and get answers from the AI assistant powered by the textbook content.</p>
              </div>
              <div className="col col--4">
                <h2>Humanoid Robotics</h2>
                <p>Explore the principles of human-inspired design in robotics systems.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}