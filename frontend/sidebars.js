// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Textbook',
      items: [
        {
          type: 'doc',
          id: 'introduction-to-physical-ai/chapter',
          label: 'Introduction to Physical AI'
        },
        {
          type: 'doc',
          id: 'foundations-of-robotics/chapter',
          label: 'Foundations of Robotics'
        },
        {
          type: 'doc',
          id: 'human-inspired-design/chapter',
          label: 'Human-Inspired Design Principles'
        }
      ]
    }
  ],
};

module.exports = sidebars;