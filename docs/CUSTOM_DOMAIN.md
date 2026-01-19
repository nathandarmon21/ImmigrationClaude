# Setting Up Custom Domain: camillegoestoamerica.com

This guide shows you how to use your own custom domain instead of the default Vercel URL.

## Step 1: Buy the Domain

### Option A: Namecheap (Recommended - Easy & Cheap)
1. Go to https://www.namecheap.com
2. Search for "camillegoestoamerica.com"
3. If available, add to cart (~$10-15/year)
4. Complete purchase
5. You now own the domain!

### Option B: GoDaddy
1. Go to https://www.godaddy.com
2. Search for domain
3. Purchase (~$12-20/year)

### Option C: Google Domains
1. Go to https://domains.google
2. Search and purchase

**Pro Tip:** Check if the `.com` is taken. Alternatives:
- `camillegoestoamerica.app`
- `camillegoestoamerica.us`
- `camillegoesto.us`

---

## Step 2: Add Domain to Vercel (After Deployment)

Once you've deployed to Vercel (see DEPLOYMENT.md):

1. **Open your Vercel project dashboard**
   - Go to https://vercel.com/dashboard
   - Click on your "camille-goes-to-america" project

2. **Go to Settings → Domains**

3. **Add your custom domain:**
   - Click "Add"
   - Enter: `camillegoestoamerica.com`
   - Click "Add"

4. **Vercel will show you DNS settings**
   - It will give you either:
     - **A Record**: Points to IP like `76.76.21.21`
     - **CNAME**: Points to something like `cname.vercel-dns.com`

---

## Step 3: Update DNS Settings

Go back to where you bought the domain (Namecheap, GoDaddy, etc.):

### For Namecheap:
1. Log in to Namecheap
2. Click "Domain List"
3. Click "Manage" next to your domain
4. Go to "Advanced DNS" tab
5. Add the records Vercel gave you:

**If Vercel gave you A Record:**
- Type: `A Record`
- Host: `@`
- Value: `76.76.21.21` (use the IP Vercel shows)
- TTL: Automatic

**If Vercel gave you CNAME:**
- Type: `CNAME Record`
- Host: `www`
- Value: `cname.vercel-dns.com` (use what Vercel shows)
- TTL: Automatic

6. Also add for non-www redirect:
- Type: `A Record`
- Host: `@`
- Value: The same IP from Vercel
- TTL: Automatic

### For GoDaddy:
1. Log in to GoDaddy
2. Go to "My Products" → "Domains"
3. Click "DNS" next to your domain
4. Click "Add" to add records from Vercel
5. Save

---

## Step 4: Wait for DNS Propagation

- **Time:** 5 minutes to 48 hours (usually ~1 hour)
- **Check status:** Go to https://www.whatsmydns.net/
- Enter your domain to see if it's working worldwide

---

## Step 5: Add SSL Certificate (Automatic!)

Vercel automatically adds a free SSL certificate (HTTPS) to your domain. This happens automatically within a few minutes of DNS propagation.

Your site will be accessible at:
- ✅ `https://camillegoestoamerica.com`
- ✅ `https://www.camillegoestoamerica.com`

---

## Costs Summary

**One-time:**
- Domain purchase: $10-20/year

**Monthly:**
- Vercel hosting: FREE
- Railway backend: FREE (with usage limits)
- Anthropic API: ~$5-20/month depending on usage

**Total:** ~$15-40/year + API costs

---

## Alternative: Use Free Vercel Subdomain

If you don't want to buy a domain yet, you can use the free Vercel subdomain:

When deploying, Vercel gives you: `camille-goes-to-america.vercel.app`

This is:
- ✅ Free forever
- ✅ Includes SSL
- ✅ Fast and reliable
- ✅ Easy to share

You can always add a custom domain later!

---

## Troubleshooting

**Domain not working after 24 hours:**
- Check DNS settings match exactly what Vercel shows
- Make sure you're using `@` for the host (not `www`)
- Clear your browser cache

**"DNS not configured" error:**
- Wait longer (can take up to 48 hours)
- Double-check you entered the records correctly

**Need help?**
- Vercel docs: https://vercel.com/docs/custom-domains
- Namecheap support: Live chat available 24/7
