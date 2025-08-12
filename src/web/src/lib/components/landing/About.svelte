<script lang="ts">
  import { onMount } from 'svelte';

  let isVisible = $state(false);

  onMount(() => {
    isVisible = true;
  });

  // Contact form state
  let formData = $state({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  let isSubmitting = $state(false);
  let submitStatus = $state<'idle' | 'success' | 'error'>('idle');

  // Form validation
  let formErrors = $derived(() => {
    const errors: Record<string, string> = {};
    
    if (!formData.name.trim()) {
      errors.name = 'Name is required';
    }
    
    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Please enter a valid email address';
    }
    
    if (!formData.subject.trim()) {
      errors.subject = 'Subject is required';
    }
    
    if (!formData.message.trim()) {
      errors.message = 'Message is required';
    }
    
    return errors;
  });

  let isFormValid = $derived(Object.keys(formErrors).length === 0);

  async function handleSubmit(event: Event) {
    event.preventDefault();
    
    if (!isFormValid || isSubmitting) return;
    
    isSubmitting = true;
    submitStatus = 'idle';
    
    try {
      // Simulate form submission - replace with actual endpoint
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Reset form on success
      formData = {
        name: '',
        email: '',
        subject: '',
        message: ''
      };
      
      submitStatus = 'success';
      console.log('📧 Contact form submitted:', formData);
    } catch (error) {
      console.error('Form submission error:', error);
      submitStatus = 'error';
    } finally {
      isSubmitting = false;
    }
  }

  function updateField(field: keyof typeof formData, value: string) {
    formData[field] = value;
  }

  // Resource categories for links section
  const resourceCategories = [
    {
      title: "Educational Resources",
      icon: "📚",
      links: [
        {
          title: "Level 1 PDF Book",
          description: "Comprehensive introduction to The Kinetic Alphabet methodology",
          url: "https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link",
        },
        {
          title: "Vulcan Tech Gospel",
          description: "Advanced technical concepts and methodologies for flow arts",
          url: "/links/vulcan-tech-gospel",
        },
        {
          title: "Charlie Cushing's 9 Square Theory",
          description: "Foundational movement analysis framework",
          url: "/links/charlie-cushing-9-square-theory",
        }
      ]
    },
    {
      title: "Flow Arts Equipment & Shops",
      icon: "🛒",
      links: [
        {
          title: "Fire & Flow",
          description: "Professional fire and LED flow arts equipment, poi, staff, and more",
          url: "https://fireandflow.com/",
        },
        {
          title: "Spin More Poi Shop",
          description: "Complete poi spinning equipment, LED poi, practice poi, and accessories",
          url: "https://www.spinmorepoi.com/shop/",
        },
        {
          title: "UltraPoi",
          description: "Premium LED poi, programming software, and advanced flow tools",
          url: "https://ultrapoi.com/",
        },
        {
          title: "Home of Poi",
          description: "Traditional and modern poi equipment, including practice and performance poi",
          url: "https://homeofpoi.com/",
        },
        {
          title: "Dark Monk",
          description: "Fire performance equipment, contact juggling balls, and practice tools",
          url: "https://www.darkmonk.com/",
        },
        {
          title: "Flowtoys",
          description: "High-quality LED flow props, poi, staff, clubs, and accessories",
          url: "https://flowtoys.com/",
        }
      ]
    },
    {
      title: "Software Tools",
      icon: "🔧",
      links: [
        {
          title: "Desktop Constructor v0.1.2",
          description: "Full-featured desktop application for sequence creation",
          url: "https://github.com/austencloud/tka-sequence-constructor/releases/download/v0.1.2/TKA_Setup.exe",
        },
        {
          title: "Web Constructor",
          description: "Browser-based sequence constructor with advanced features (you're using it now!)",
          url: "/constructor",
        },
        {
          title: "Sequence Animator",
          description: "View and animate existing sequences with advanced playback controls",
          url: "/animator",
        }
      ]
    },
    {
      title: "Community & Development",
      icon: "🤝",
      links: [
        {
          title: "GitHub Repository",
          description: "Source code and development updates",
          url: "https://github.com/austencloud/tka-sequence-constructor",
        },
        {
          title: "Flow Arts Resources",
          description: "External community links and tutorials",
          url: "https://www.spinmorepoi.com/",
        }
      ]
    },
    {
      title: "Flow Arts Community",
      icon: "🌟",
      links: [
        {
          title: "Poi Spinning Community",
          description: "Global community for poi spinners and flow artists",
          url: "https://www.reddit.com/r/poi/",
        },
        {
          title: "Flow Arts Institute",
          description: "Educational resources and workshops",
          url: "https://flowartsinstitute.com/",
        },
        {
          title: "Spin More Poi",
          description: "Comprehensive poi spinning tutorials and community",
          url: "https://www.spinmorepoi.com/",
        }
      ]
    }
  ];

  function handleLinkClick(url: string) {
    console.log(`🔗 Link clicked: ${url}`);
  }
</script>

<svelte:head>
  <title>About - The Kinetic Alphabet</title>
  <meta name="description" content="Learn about The Kinetic Alphabet project, get in touch, and find resources for flow arts education." />
</svelte:head>

<main class="about-container">
  <!-- Hero Section -->
  <section class="hero" class:visible={isVisible}>
    <div class="hero-content">
      <h1 class="hero-title">About The Kinetic Alphabet</h1>
      <p class="hero-subtitle">Innovation in Flow Arts Education</p>
    </div>
  </section>

  <!-- Philosophy Section -->
  <section class="philosophy">
    <div class="container">
      <h2>Philosophy</h2>
      <div class="philosophy-content">
        <p>
          The Kinetic Alphabet represents a paradigm shift in how flow artists approach their craft. 
          By providing a systematic framework for understanding movement, we enable practitioners 
          to develop deeper technical skills while preserving the artistic freedom that defines flow arts.
        </p>
        <p>
          Our approach combines rigorous technical methodology with creative expression, 
          allowing artists to build a solid foundation while exploring infinite possibilities 
          for personal artistic development.
        </p>
      </div>
    </div>
  </section>

  <!-- Quick Access Section -->
  <section class="quick-access">
    <div class="container">
      <h2>Quick Access</h2>
      <div class="quick-grid">
        <button 
          onclick={() => window.location.href = '/constructor'} 
          class="quick-link constructor"
        >
          <div class="quick-icon">🔧</div>
          <div class="quick-content">
            <h3>Start Creating</h3>
            <p>Jump into the constructor</p>
          </div>
        </button>

        <a 
          href="https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link" 
          target="_blank" 
          rel="noopener noreferrer" 
          class="quick-link learn"
        >
          <div class="quick-icon">📚</div>
          <div class="quick-content">
            <h3>Learn the Basics</h3>
            <p>Download Level 1 PDF</p>
          </div>
        </a>

        <a 
          href="https://github.com/austencloud/tka-sequence-constructor/releases/download/v0.1.2/TKA_Setup.exe" 
          class="quick-link download"
          target="_blank"
          rel="noopener noreferrer"
        >
          <div class="quick-icon">⬇️</div>
          <div class="quick-content">
            <h3>Get Desktop App</h3>
            <p>Download v0.1.2</p>
          </div>
        </a>
      </div>
    </div>
  </section>

  <!-- Project Overview -->
  <section class="project-overview">
    <div class="container">
      <h2>The Project</h2>
      <div class="overview-grid">
        <div class="overview-card">
          <h3>🎯 Mission</h3>
          <p>
            To provide systematic tools and methodologies that enhance technical precision 
            and creative expression in flow arts through structured learning approaches.
          </p>
        </div>

        <div class="overview-card">
          <h3>🔬 Methodology</h3>
          <p>
            The system breaks down complex movements into understandable components, 
            creating a notation system that enables precise communication and analysis.
          </p>
        </div>

        <div class="overview-card">
          <h3>🌟 Vision</h3>
          <p>
            A global community of flow artists connected through shared language 
            and collaborative tools for sequence creation and knowledge sharing.
          </p>
        </div>

        <div class="overview-card">
          <h3>🛠️ Tools</h3>
          <p>
            Digital applications that support visualization, creation, and sharing 
            of choreographic sequences across multiple flow art disciplines.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="features">
    <div class="container">
      <h2>The Kinetic Alphabet Features</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">📚</div>
          <h3>Systematic Learning</h3>
          <p>Complex movements are broken down into understandable components through a structured notation system.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>Precision Training</h3>
          <p>The system supports muscle memory development and technical precision through methodical movement approaches.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🔧</div>
          <h3>Digital Tools</h3>
          <p>The Kinetic Constructor enables visualization, creation, and sharing of choreographic sequences.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🌟</div>
          <h3>Creative Framework</h3>
          <p>The system provides foundational knowledge that enables exploration of infinite sequence possibilities.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Getting Started Section -->
  <section class="getting-started">
    <div class="container">
      <h2>Getting Started</h2>
      <div class="steps-grid">
        <div class="step">
          <div class="step-number">1</div>
          <h3>Download the PDF</h3>
          <p>The comprehensive Level 1 guide introduces core concepts and foundational principles.</p>
        </div>

        <div class="step">
          <div class="step-number">2</div>
          <h3>Practice the Basics</h3>
          <p>Fundamental movements and notation system can be learned through guided exercises.</p>
        </div>

        <div class="step">
          <div class="step-number">3</div>
          <h3>Use the Constructor</h3>
          <p>The web-based constructor allows creation and visualization of custom sequences.</p>
        </div>

        <div class="step">
          <div class="step-number">4</div>
          <h3>Join the Community</h3>
          <p>Connect with flow artists and share creations through our growing community platform.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Resources & Links Section -->
  <section class="resources-links">
    <div class="container">
      <h2>Resources & Links</h2>
      <div class="resources-grid">
        {#each resourceCategories as category}
          <div class="resource-category">
            <div class="category-header">
              <div class="category-icon">{category.icon}</div>
              <h3 class="category-title">{category.title}</h3>
            </div>
            <div class="links-list">
              {#each category.links as link}
                <a
                  href={link.url}
                  target={link.url.startsWith('http') ? '_blank' : '_self'}
                  rel={link.url.startsWith('http') ? 'noopener noreferrer' : ''}
                  class="resource-link"
                  onclick={() => handleLinkClick(link.url)}
                >
                  <div class="link-content">
                    <h4 class="link-title">{link.title}</h4>
                    <p class="link-description">{link.description}</p>
                  </div>
                  <div class="link-arrow">→</div>
                </a>
              {/each}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- Contact Section -->
  <section class="contact-section">
    <div class="container">
      <div class="contact-grid">
        <!-- Contact Information -->
        <div class="contact-info">
          <h2>Get In Touch</h2>
          
          <div class="info-card">
            <div class="info-icon">📧</div>
            <div class="info-content">
              <h3>Email</h3>
              <p>tkaflowarts@gmail.com</p>
              <a href="mailto:tkaflowarts@gmail.com" class="contact-link">
                Send us an email
              </a>
            </div>
          </div>

          <div class="info-card">
            <div class="info-icon">🔧</div>
            <div class="info-content">
              <h3>Technical Support</h3>
              <p>Need help with the Constructor or other tools?</p>
              <a href="mailto:tkaflowarts@gmail.com?subject=Technical Support" class="contact-link">
                Get technical help
              </a>
            </div>
          </div>

          <div class="info-card">
            <div class="info-icon">🤝</div>
            <div class="info-content">
              <h3>Collaborations</h3>
              <p>Interested in partnerships or contributing?</p>
              <a href="mailto:tkaflowarts@gmail.com?subject=Collaboration" class="contact-link">
                Discuss collaboration
              </a>
            </div>
          </div>
        </div>

        <!-- Contact Form -->
        <div class="contact-form-section">
          <h2>Send Us a Message</h2>
          
          <form class="contact-form" onsubmit={handleSubmit}>
            <!-- Name Field -->
            <div class="form-group">
              <label for="name" class="form-label">Name *</label>
              <input
                type="text"
                id="name"
                class="form-input"
                class:error={formErrors.name}
                value={formData.name}
                oninput={(e) => updateField('name', e.currentTarget.value)}
                placeholder="Your name"
                required
              />
              {#if formErrors.name}
                <span class="error-message">{formErrors.name}</span>
              {/if}
            </div>

            <!-- Email Field -->
            <div class="form-group">
              <label for="email" class="form-label">Email *</label>
              <input
                type="email"
                id="email"
                class="form-input"
                class:error={formErrors.email}
                value={formData.email}
                oninput={(e) => updateField('email', e.currentTarget.value)}
                placeholder="your.email@example.com"
                required
              />
              {#if formErrors.email}
                <span class="error-message">{formErrors.email}</span>
              {/if}
            </div>

            <!-- Subject Field -->
            <div class="form-group">
              <label for="subject" class="form-label">Subject *</label>
              <input
                type="text"
                id="subject"
                class="form-input"
                class:error={formErrors.subject}
                value={formData.subject}
                oninput={(e) => updateField('subject', e.currentTarget.value)}
                placeholder="What's this about?"
                required
              />
              {#if formErrors.subject}
                <span class="error-message">{formErrors.subject}</span>
              {/if}
            </div>

            <!-- Message Field -->
            <div class="form-group">
              <label for="message" class="form-label">Message *</label>
              <textarea
                id="message"
                class="form-textarea"
                class:error={formErrors.message}
                value={formData.message}
                oninput={(e) => updateField('message', e.currentTarget.value)}
                placeholder="Tell us what's on your mind..."
                rows="6"
                required
              ></textarea>
              {#if formErrors.message}
                <span class="error-message">{formErrors.message}</span>
              {/if}
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              class="submit-button"
              disabled={!isFormValid || isSubmitting}
            >
              {#if isSubmitting}
                <span class="button-spinner">
                  <svg viewBox="0 0 24 24" width="16" height="16">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none"/>
                    <path d="M12,2 A10,10 0 0,1 22,12" stroke="currentColor" stroke-width="2" fill="none">
                      <animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
                    </path>
                  </svg>
                </span>
                Sending...
              {:else}
                Send Message
              {/if}
            </button>

            <!-- Status Messages -->
            {#if submitStatus === 'success'}
              <div class="status-message success">
                ✅ Message sent successfully! We'll get back to you soon.
              </div>
            {:else if submitStatus === 'error'}
              <div class="status-message error">
                ❌ Failed to send message. Please try again or email us directly.
              </div>
            {/if}
          </form>
        </div>
      </div>
    </div>
  </section>
</main>

<style>
  .about-container {
    min-height: 100vh;
    padding: 0;
    overflow-y: auto;
    overflow-x: hidden;
  }

  /* Hero Section */
  .hero {
    position: relative;
    color: var(--text-color);
    padding: var(--spacing-3xl) 0 var(--spacing-2xl) 0;
    text-align: center;
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s ease;
    z-index: 1;
    min-height: 40vh;
    display: flex;
    align-items: center;

    /* Glassmorphism styling */
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 2rem;
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    margin: var(--spacing-lg);
  }

  .hero.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .hero-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 var(--spacing-xl);
  }

  .hero-title {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-subtitle {
    font-size: 1.25rem;
    opacity: 0.9;
    font-weight: 300;
  }

  /* Content Sections */
  .philosophy,
  .project-overview,
  .resources-links,
  .contact-section {
    padding: var(--spacing-3xl) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2.5rem;
    font-weight: 700;
  }

  /* Philosophy Section */
  .philosophy-content {
    max-width: 800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: var(--spacing-xl);
    border-radius: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .philosophy-content p {
    font-size: 1.125rem;
    line-height: 1.8;
    margin-bottom: var(--spacing-lg);
    color: rgba(255, 255, 255, 0.9);
  }

  /* Project Overview */
  .overview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--spacing-xl);
  }

  .overview-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: var(--spacing-xl);
    border-radius: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
  }

  .overview-card:hover {
    transform: translateY(-5px);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .overview-card h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-size: 1.25rem;
    font-weight: 600;
  }

  .overview-card p {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
  }

  /* Features Section */
  .features {
    padding: var(--spacing-3xl) 0;
  }

  .features h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2.5rem;
    font-weight: 700;
  }

  .features-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: var(--spacing-xl);
    margin-top: var(--spacing-2xl);
    align-items: stretch;
  }

  .feature-card {
    position: relative;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: var(--spacing-xl);
    border-radius: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    transition: all 0.3s ease;
  }

  .feature-card:hover {
    transform: translateY(-10px) scale(1.02);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 
      0 20px 40px rgba(118, 75, 162, 0.2),
      0 8px 20px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .feature-icon {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    display: inline-block;
    transition: all 0.3s ease;
  }

  .feature-card:hover .feature-icon {
    transform: scale(1.1) rotate(5deg);
  }

  .feature-card h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-weight: 700;
    font-size: 1.25rem;
  }

  .feature-card p {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
  }

  /* Getting Started Section */
  .getting-started {
    padding: var(--spacing-3xl) 0;
  }

  .getting-started h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2.5rem;
    font-weight: 700;
  }

  .steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-xl);
    margin-top: var(--spacing-2xl);
  }

  .step {
    text-align: center;
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.03);
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
  }

  .step:hover {
    background: rgba(255, 255, 255, 0.06);
    transform: translateY(-3px);
  }

  .step-number {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0 auto var(--spacing-md) auto;
  }

  .step h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-weight: 600;
  }

  .step p {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
  }

  /* Quick Access Section */
  .quick-access {
    padding: var(--spacing-3xl) 0;
    background: rgba(255, 255, 255, 0.02);
  }

  .quick-access h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2rem;
    font-weight: 700;
  }

  .quick-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-lg);
    max-width: 900px;
    margin: 0 auto;
  }

  .quick-link {
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease;
    cursor: pointer;
  }

  .quick-link:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
  }

  .quick-link.constructor:hover {
    border-color: rgba(102, 126, 234, 0.4);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
  }

  .quick-link.learn:hover {
    border-color: rgba(34, 197, 94, 0.4);
    box-shadow: 0 8px 20px rgba(34, 197, 94, 0.2);
  }

  .quick-link.download:hover {
    border-color: rgba(249, 115, 22, 0.4);
    box-shadow: 0 8px 20px rgba(249, 115, 22, 0.2);
  }

  .quick-icon {
    font-size: 2rem;
    flex-shrink: 0;
  }

  .quick-content h3 {
    color: var(--text-color);
    font-weight: 600;
    margin: 0 0 4px 0;
  }

  .quick-content p {
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    font-size: var(--font-size-sm);
  }

  /* Resources & Links Section */
  .resources-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: var(--spacing-2xl);
  }

  .resource-category {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: var(--spacing-xl);
    border-radius: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .category-header {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
  }

  .category-icon {
    font-size: 2rem;
  }

  .category-title {
    color: var(--text-color);
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
  }

  .links-list {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .resource-link {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
  }

  .resource-link:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateX(4px);
  }

  .link-content {
    flex: 1;
  }

  .link-title {
    color: var(--text-color);
    font-weight: 600;
    margin: 0 0 4px 0;
    font-size: 1rem;
  }

  .link-description {
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    font-size: var(--font-size-sm);
  }

  .link-arrow {
    color: #667eea;
    font-weight: bold;
    opacity: 0.7;
    transition: opacity 0.2s ease;
  }

  .resource-link:hover .link-arrow {
    opacity: 1;
  }

  /* Contact Section */
  .contact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-3xl);
    align-items: start;
  }

  /* Contact Info */
  .contact-info h2,
  .contact-form-section h2 {
    color: var(--text-color);
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: var(--spacing-xl);
  }

  .info-card {
    display: flex;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    margin-bottom: var(--spacing-lg);
    transition: all 0.3s ease;
  }

  .info-card:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-2px);
  }

  .info-icon {
    font-size: 2rem;
    flex-shrink: 0;
  }

  .info-content h3 {
    color: var(--text-color);
    font-weight: 600;
    margin-bottom: var(--spacing-sm);
  }

  .info-content p {
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: var(--spacing-sm);
    line-height: 1.5;
  }

  .contact-link {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s ease;
  }

  .contact-link:hover {
    color: #764ba2;
    text-decoration: underline;
  }

  /* Contact Form */
  .contact-form {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1.5rem;
    padding: var(--spacing-xl);
  }

  .form-group {
    margin-bottom: var(--spacing-lg);
  }

  .form-label {
    display: block;
    color: var(--text-color);
    font-weight: 600;
    margin-bottom: var(--spacing-sm);
  }

  .form-input,
  .form-textarea {
    width: 100%;
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    color: var(--text-color);
    font-size: var(--font-size-base);
    transition: all 0.2s ease;
    box-sizing: border-box;
  }

  .form-input::placeholder,
  .form-textarea::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }

  .form-input:focus,
  .form-textarea:focus {
    outline: none;
    border-color: #667eea;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
  }

  .form-input.error,
  .form-textarea.error {
    border-color: #ff6b6b;
    box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2);
  }

  .form-textarea {
    resize: vertical;
    min-height: 120px;
  }

  .error-message {
    display: block;
    color: #ff6b6b;
    font-size: var(--font-size-sm);
    margin-top: var(--spacing-xs);
  }

  .submit-button {
    width: 100%;
    padding: var(--spacing-md) var(--spacing-lg);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: var(--border-radius);
    font-size: var(--font-size-base);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
  }

  .submit-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }

  .submit-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .button-spinner {
    display: flex;
    align-items: center;
  }

  .status-message {
    margin-top: var(--spacing-md);
    padding: var(--spacing-md);
    border-radius: var(--border-radius);
    text-align: center;
    font-weight: 500;
  }

  .status-message.success {
    background: rgba(34, 197, 94, 0.2);
    color: #22c55e;
    border: 1px solid rgba(34, 197, 94, 0.3);
  }

  .status-message.error {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .hero {
      padding: var(--spacing-2xl) 0;
      min-height: 30vh;
      margin: var(--spacing-md);
    }

    .hero-title {
      font-size: 2.5rem;
    }

    .hero-subtitle {
      font-size: 1.125rem;
    }

    .features,
    .getting-started,
    .quick-access,
    .philosophy,
    .project-overview,
    .resources-links,
    .contact-section {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    h2 {
      font-size: 2rem;
    }

    .philosophy-content,
    .contact-form {
      padding: var(--spacing-lg);
    }

    .overview-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }

    .features-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, auto);
      gap: var(--spacing-lg);
    }

    .steps-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }

    .quick-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }

    .quick-link {
      padding: var(--spacing-md);
    }

    .resources-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }

    .contact-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-2xl);
    }

    .info-card {
      padding: var(--spacing-md);
    }

    .form-group {
      margin-bottom: var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .hero {
      transition: none;
      opacity: 1;
      transform: none;
    }

    .overview-card,
    .resource-link,
    .info-card,
    .submit-button {
      transition: none;
    }

    .overview-card:hover,
    .resource-link:hover,
    .info-card:hover,
    .submit-button:hover {
      transform: none;
    }
  }
</style>
