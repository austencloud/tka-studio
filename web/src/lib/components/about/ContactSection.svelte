<script lang="ts">
  import { browser } from "$app/environment";

  let formData = $state({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  let isSubmitting = $state(false);
  let submitStatus = $state<"idle" | "success" | "error">("idle");

  const socialLinks = [
    {
      name: "GitHub",
      url: "https://github.com/yourusername",
      icon: "github",
      description: "Source code and project repositories",
    },
    {
      name: "YouTube",
      url: "https://youtube.com/@yourchannel",
      icon: "youtube",
      description: "Tutorial videos and flow arts content",
    },
    {
      name: "Instagram",
      url: "https://instagram.com/yourusername",
      icon: "instagram",
      description: "Visual content and community updates",
    },
    {
      name: "Discord",
      url: "https://discord.gg/yourinvite",
      icon: "discord",
      description: "Join our flow arts community",
    },
    {
      name: "Reddit",
      url: "https://reddit.com/r/flowarts",
      icon: "reddit",
      description: "Flow arts discussions and sharing",
    },
    {
      name: "Email",
      url: "mailto:contact@kineticalphabetproject.com",
      icon: "email",
      description: "Direct contact for inquiries",
    },
  ];

  function validateEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();

    if (
      !formData.name.trim() ||
      !formData.email.trim() ||
      !formData.message.trim()
    ) {
      submitStatus = "error";
      return;
    }

    if (!validateEmail(formData.email)) {
      submitStatus = "error";
      return;
    }

    isSubmitting = true;
    submitStatus = "idle";

    try {
      // Simulate form submission (replace with actual API call)
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Reset form on success
      formData = { name: "", email: "", subject: "", message: "" };
      submitStatus = "success";
    } catch (error) {
      submitStatus = "error";
    } finally {
      isSubmitting = false;
    }
  }

  function openSocialLink(url: string) {
    if (browser) {
      window.open(url, "_blank", "noopener,noreferrer");
    }
  }
</script>

<!-- Contact Section -->
<section class="contact-section">
  <div class="container">
    <div class="contact-grid">
      <!-- Contact Info -->
      <div class="contact-info">
        <h2>Get in Touch</h2>
        <p class="contact-description">
          Have questions about The Kinetic Alphabet? Want to contribute to the
          project or share feedback? I'd love to hear from you!
        </p>

        <div class="contact-methods">
          <div class="contact-method">
            <div class="method-icon">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <polyline
                  points="22,6 12,13 2,6"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>
            <div class="method-details">
              <h3>Email</h3>
              <p>contact@kineticalphabetproject.com</p>
              <span class="method-note"
                >Best for detailed inquiries and collaboration</span
              >
            </div>
          </div>

          <div class="contact-method">
            <div class="method-icon">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M9 19c-5 0-8-3-8-8s3-8 8-8 8 3 8 8-3 8-8 8z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  d="M9 9a3 3 0 0 1 3 3"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  d="M9 5a7 7 0 0 1 7 7"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>
            <div class="method-details">
              <h3>Response Time</h3>
              <p>24-48 hours typically</p>
              <span class="method-note"
                >I aim to respond to all messages promptly</span
              >
            </div>
          </div>
        </div>

        <!-- Social Media Links -->
        <div class="social-section">
          <h3>Connect & Follow</h3>
          <p>
            Join the community and stay updated with the latest developments:
          </p>

          <div class="social-grid">
            {#each socialLinks as social}
              <button
                class="social-link"
                onclick={() => openSocialLink(social.url)}
                type="button"
              >
                <div class="social-icon">
                  {#if social.icon === "github"}
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
                      />
                    </svg>
                  {:else if social.icon === "youtube"}
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"
                      />
                    </svg>
                  {:else if social.icon === "instagram"}
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"
                      />
                    </svg>
                  {:else if social.icon === "discord"}
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419-.0003 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1568 2.4189Z"
                      />
                    </svg>
                  {:else if social.icon === "reddit"}
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                    >
                      <path
                        d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"
                      />
                    </svg>
                  {:else if social.icon === "email"}
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                    >
                      <path
                        d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <polyline
                        points="22,6 12,13 2,6"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                    </svg>
                  {/if}
                </div>
                <div class="social-content">
                  <span class="social-name">{social.name}</span>
                  <span class="social-description">{social.description}</span>
                </div>
              </button>
            {/each}
          </div>
        </div>
      </div>

      <!-- Contact Form -->
      <div class="contact-form-container">
        <form class="contact-form" onsubmit={handleSubmit}>
          <h3>Send a Message</h3>

          <div class="form-row">
            <div class="form-group">
              <label for="name">Name *</label>
              <input
                type="text"
                id="name"
                bind:value={formData.name}
                required
                placeholder="Your name"
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label for="email">Email *</label>
              <input
                type="email"
                id="email"
                bind:value={formData.email}
                required
                placeholder="your.email@example.com"
                class="form-input"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="subject">Subject</label>
            <input
              type="text"
              id="subject"
              bind:value={formData.subject}
              placeholder="What's this about?"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="message">Message *</label>
            <textarea
              id="message"
              bind:value={formData.message}
              required
              placeholder="Tell me about your question, suggestion, or how you'd like to contribute..."
              rows="6"
              class="form-textarea"
            ></textarea>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            class="submit-button"
            class:submitting={isSubmitting}
          >
            {#if isSubmitting}
              <svg class="spinner" width="20" height="20" viewBox="0 0 24 24">
                <circle
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="2"
                  fill="none"
                  opacity="0.25"
                />
                <path
                  d="M12 2a10 10 0 0 1 10 10"
                  stroke="currentColor"
                  stroke-width="2"
                  fill="none"
                />
              </svg>
              Sending...
            {:else}
              Send Message
            {/if}
          </button>

          {#if submitStatus === "success"}
            <div class="status-message success">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
              >
                <polyline
                  points="20,6 9,17 4,12"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              Thank you! Your message has been sent successfully.
            </div>
          {:else if submitStatus === "error"}
            <div class="status-message error">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
              >
                <circle cx="12" cy="12" r="10" stroke-width="2" />
                <line x1="15" y1="9" x2="9" y2="15" stroke-width="2" />
                <line x1="9" y1="9" x2="15" y2="15" stroke-width="2" />
              </svg>
              Please check your information and try again.
            </div>
          {/if}
        </form>
      </div>
    </div>
  </div>
</section>

<style>
  /* Contact Section */
  .contact-section {
    padding: var(--spacing-3xl) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  .contact-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-3xl);
    align-items: start;
  }

  /* Contact Info */
  .contact-info h2 {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
  }

  .contact-description {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: var(--spacing-2xl);
  }

  .contact-methods {
    margin-bottom: var(--spacing-2xl);
  }

  .contact-method {
    display: flex;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-lg);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
  }

  .method-icon {
    flex-shrink: 0;
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: var(--border-radius);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }

  .method-details h3 {
    font-size: var(--font-size-lg);
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: var(--spacing-xs);
  }

  .method-details p {
    font-size: var(--font-size-base);
    color: var(--primary-color);
    margin-bottom: var(--spacing-xs);
    font-weight: 500;
  }

  .method-note {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }

  /* Social Section */
  .social-section {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-xl);
  }

  .social-section h3 {
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: var(--spacing-sm);
  }

  .social-section > p {
    color: var(--text-secondary);
    margin-bottom: var(--spacing-lg);
    line-height: 1.6;
  }

  .social-grid {
    display: grid;
    gap: var(--spacing-sm);
  }

  .social-link {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
    color: var(--text-color);
    text-decoration: none;
    transition: all 0.3s ease;
    cursor: pointer;
    font-family: inherit;
    text-align: left;
    width: 100%;
  }

  .social-link:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: var(--primary-color);
    transform: translateX(4px);
  }

  .social-icon {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary-color);
  }

  .social-content {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .social-name {
    font-weight: 600;
    color: var(--text-color);
  }

  .social-description {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
  }

  /* Contact Form */
  .contact-form-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-xl);
  }

  .contact-form h3 {
    font-size: var(--font-size-xl);
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: var(--spacing-lg);
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-md);
  }

  .form-group {
    margin-bottom: var(--spacing-md);
  }

  .form-group label {
    display: block;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: var(--spacing-xs);
    font-size: var(--font-size-sm);
  }

  .form-input,
  .form-textarea {
    width: 100%;
    padding: var(--spacing-md);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    color: var(--text-color);
    font-family: inherit;
    font-size: var(--font-size-base);
    transition: all 0.3s ease;
  }

  .form-input:focus,
  .form-textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-2px);
  }

  .form-input::placeholder,
  .form-textarea::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }

  .form-textarea {
    resize: vertical;
    min-height: 120px;
  }

  .submit-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: var(--spacing-md) var(--spacing-xl);
    border-radius: var(--border-radius-lg);
    font-family: inherit;
    font-size: var(--font-size-base);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
    min-height: 48px;
  }

  .submit-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }

  .submit-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .spinner {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .status-message {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    border-radius: var(--border-radius);
    margin-top: var(--spacing-md);
    font-weight: 500;
  }

  .status-message.success {
    background: rgba(76, 175, 80, 0.1);
    color: #4caf50;
    border: 1px solid rgba(76, 175, 80, 0.2);
  }

  .status-message.error {
    background: rgba(244, 67, 54, 0.1);
    color: #f44336;
    border: 1px solid rgba(244, 67, 54, 0.2);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .contact-section {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    .contact-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-2xl);
    }

    .contact-info h2 {
      font-size: 2rem;
    }

    .contact-method {
      flex-direction: column;
      text-align: center;
      gap: var(--spacing-sm);
    }

    .method-icon {
      align-self: center;
    }

    .form-row {
      grid-template-columns: 1fr;
    }

    .contact-form-container,
    .social-section {
      padding: var(--spacing-md);
    }

    .social-link:hover {
      transform: none;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .submit-button,
    .social-link,
    .form-input,
    .form-textarea {
      transition: none;
    }

    .submit-button:hover,
    .social-link:hover,
    .form-input:focus,
    .form-textarea:focus {
      transform: none;
    }

    .spinner {
      animation: none;
    }
  }
</style>
