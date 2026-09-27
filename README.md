# Team R2 website: how to finish and publish

This `site` folder is the complete website. Upload everything in it (html files, `css`, `js`, `images`, `sitemap.xml`, `robots.txt`) to the web root of whatever host you pick. `build.py` and this README don't need to be uploaded.

Open `index.html` in a browser to preview it locally.

## Before you go live (checklist)

1. **Contact form: connected** (Web3Forms key is set in `build.py`; send a test from the live site)
   - Go to https://web3forms.com, enter `info@TeamR2.com`, and they email you an access key.
   - Paste the key into `build.py` → `"web3forms_key"` and run `python build.py`,
     **or** open `contact.html` and replace `YOUR_WEB3FORMS_ACCESS_KEY`.
   - Until you do this, the form tells visitors to email info@TeamR2.com instead.
   - Submissions arrive by email with every field (request type, company, bid date, duct types, drawings link…).
   - The free plan doesn't accept file uploads, so the form asks for a *link* to drawings. If you want uploads later, Web3Forms Pro or Formspree paid plans support them.
2. **Already set:** Indeed link (`indeed.com/cmp/R2-Fabrication-1/jobs`), 80,000 sq. ft., phone 817.720.6060, and hours Mon–Fri 7:00 am – 3:30 pm. You can change any of them in `build.py` → `S`.
3. **Review these items.** Search the html for `CONFIRM` and `IDEA` comments:
   - `equipment.html`: confirmed so far are the CNC plasma table, CNC laser table, and 2 spiral machines. The rest (coil line, roll formers, shears, press brakes, ironworker, welders) I worked out from photos. Add counts, capacities, and makes if you want them shown.
   - `installation-services.html`: the "What our crews install" list.
   - `about.html`: a commented-out block for EMR, SMACNA edition, OSHA training, and license numbers (GCs ask for these).
   - `careers.html`: a comment listing typical roles you could add.
4. **Privacy Policy and SMS Terms.** I rebuilt these from the pages on your current live site. Compare them with your originals, since your SMS (10DLC) registration may depend on the exact wording.
5. **Photos (planned).** New photos are coming. To swap one in, save it as `images/full/NN.jpg` (about 1600px wide) plus `images/thumb/NN.jpg` (640px) using the same number, or add new numbers and reference them in `build.py`.

## Editing later

- **Easy way:** edit the settings or page text in `build.py`, then run `python build.py` (Python 3.8+, no installs). It regenerates every page with the same header and footer.
- **Direct way:** edit any `.html` file. The header and footer are repeated in each file, so a nav change means editing every page. That's why `build.py` exists.

## Hosting options (static, all fine)

| Host | Cost | Notes |
|---|---|---|
| Cloudflare Pages / Netlify | Free | Drag-and-drop the folder or connect a Git repo. Free SSL. `/about` works as well as `/about.html`. |
| Azure Static Web Apps | Free tier | Good fit if you're already in Microsoft 365/Azure. |
| Your IIS server | – | Copy the folder to the site root and set `404.html` as the custom 404 page. |
| Current host (GoDaddy/Wix/etc.) | – | Any host that serves plain HTML works. Wix and Squarespace don't. |

**Keep old links working.** The live site uses paths like `/fabrication-hvac`, `/installation-services1`, and `/location`. The new file names match except these:
- `/installation-services1` → set a redirect to `/installation-services.html` (Netlify/Cloudflare: add a `_redirects` file with `/installation-services1 /installation-services.html 301`)
- `/location` → `location.html` already forwards to the map on the Contact page.

After launch, submit `https://www.teamr2.com/sitemap.xml` in Google Search Console and update your Google Business Profile's website link.

## Files

```
index.html                 Home
fabrication-hvac.html      HVAC ductwork
fabrication-misc.html      Industrial fabrication
installation-services.html Installation
equipment.html             Shop & equipment (new)
about.html                 About + safety/standards
careers.html               Careers → Indeed
contact.html               Bid request form + map
thanks.html, 404.html, location.html (redirect), privacy-policy.html, sms.html
css/style.css   js/site.js   images/   sitemap.xml   robots.txt   build.py
```

Brand colors: orange `#FF6700`, black `#111111`, grey `#7B7D82` (sampled from the new logo). Fonts: Barlow / Barlow Condensed (Google Fonts).
