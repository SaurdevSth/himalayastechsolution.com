# Deploying himalayastechsolution.com to your DigitalOcean droplet

This package contains:

- `site/` – the website (upload this folder)
  - `index.html` (home), `web-design/`, `seo/`, `cloud-gpu/`, `it-solutions/`, `404.html`
  - `assets/` – favicon, app icon, logo and the social sharing image
  - `robots.txt` and `sitemap.xml` for Google
- `deploy/nginx.conf` – the web server settings

Replace `YOUR_DROPLET_IP` below with your droplet's IP address (shown in the DigitalOcean dashboard).

---

## 1. Point the domain at the droplet

At your domain registrar, or in DigitalOcean under **Networking → Domains**, add:

| Type | Name | Value |
|------|------|-------|
| A | `@` | `YOUR_DROPLET_IP` |
| A | `www` | `YOUR_DROPLET_IP` |

If your email (business@himalayastechsolution.com) is already set up, leave its MX records alone. Only add or change the two A records.

DNS changes can take from a few minutes to a few hours.

## 2. Install the web server (one time)

Connect to the droplet:

```bash
ssh root@YOUR_DROPLET_IP
```

Then run:

```bash
sudo apt update
sudo apt install -y nginx
sudo ufw allow 'Nginx Full'
sudo mkdir -p /var/www/himalayastechsolution.com
```

## 3. Upload the website

Clone this repository. From the repository folder, run (on your computer, not the droplet):

```bash
scp -r site/* root@YOUR_DROPLET_IP:/var/www/himalayastechsolution.com/
scp deploy/nginx.conf root@YOUR_DROPLET_IP:/etc/nginx/sites-available/himalayastechsolution.com
```

## 4. Turn the site on

Back on the droplet:

```bash
sudo ln -s /etc/nginx/sites-available/himalayastechsolution.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

`nginx -t` should say the configuration is OK. If this droplet hosts only this site, you can also remove the placeholder site with `sudo rm /etc/nginx/sites-enabled/default` before reloading. Don't remove it if other sites run on this droplet.

## 5. Add HTTPS (free certificate)

Once the domain points to the droplet (step 1), run:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d himalayastechsolution.com -d www.himalayastechsolution.com --redirect
```

Certbot asks for an email and sets up automatic renewal. Your site is now live at **https://himalayastechsolution.com**.

## 6. Tell Google about it

1. Go to Google Search Console and add `himalayastechsolution.com` as a domain property.
2. Verify ownership with the DNS record it gives you.
3. Under **Sitemaps**, submit `https://himalayastechsolution.com/sitemap.xml`.

## Updating the site later

Upload the changed files the same way:

```bash
scp -r site/* root@YOUR_DROPLET_IP:/var/www/himalayastechsolution.com/
```

Changes show immediately; there's no need to restart anything.
