# 🔧 UPDATE YOUR CATEGORIES - SIMPLE INSTRUCTIONS

## Option 1: Use Your Browser (EASIEST - 30 seconds)

1. **Open this URL in your browser:**
   ```
   https://sandy-adhd-coach-production.up.railway.app/admin/fix-descriptions
   ```

2. **You'll be redirected to login** - Use your credentials:
   - Email: `user@example.com`
   - Password: `string`

3. **Done!** The endpoint will automatically update all 18 categories.

---

## Option 2: Use Telegram

Just talk to Sandy on Telegram and she'll use the updated descriptions immediately!

---

## Option 3: Use curl (If You Want Command Line)

### Step 1: Get Your JWT Token

1. Go to: https://sandy-adhd-coach-production.up.railway.app
2. Log in with: `user@example.com` / `string`
3. Open browser DevTools (F12)
4. Go to: **Application → Local Storage**
5. Find: `access_token`
6. Copy the value (a long string like `eyJ0eXAiOiJKV1...`)

### Step 2: Run This Command

```bash
curl -X POST "https://sandy-adhd-coach-production.up.railway.app/admin/fix-descriptions" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json"
```

Replace `YOUR_JWT_TOKEN_HERE` with the token from Step 1.

---

## How to Verify It Worked

### Test on Telegram:
1. Send: `/explore`
2. Should say: **"What actually gets YOU started"** ✅
3. NOT: "What actually gets HIM started" ❌

### Or check the response:
The endpoint returns:
```json
{
  "success": true,
  "message": "Updated 18 category descriptions from 'him/he' to 'you'",
  "updated_count": 18
}
```

---

## What Gets Updated

All 18 categories in your database:
- ✅ task_initiation → "What actually gets **you** started"
- ✅ hyperfocus_triggers → "What puts **you** in the zone"
- ✅ avoidance_reasons → "WHY **you** avoid specific tasks"
- ... and 15 more

---

## 🎯 Recommended: Use Option 1 (Browser)

**Just click this link and log in:**
https://sandy-adhd-coach-production.up.railway.app/admin/fix-descriptions

Takes 30 seconds!

