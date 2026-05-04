import urllib.request
import os

screens = [
    {
        "name": "France",
        "img_url": "https://lh3.googleusercontent.com/aida/ADBb0ugBAg6YeQau8vI8QEpluR4BeOU-nnrQG37FmaNicuf32qielD1UqXQmAXlT33blROFjmeWCYtyW7oARvXb9_KcD77n65HUxyi1sJRsGiK3cloRK40aUaVkJrZrNcdjB34eT02dC5x1PcD500VmiCPQ_9K0VGAD2dGPaUvfx9rEZ0dwpnig-1ClSescI_RBs5GlpWkMBONhp7qWyx88Fp79THEJr4peaFdt-mT3p_rwDwHEUXn4xwW84NTI",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzU0ZDg4NmJhMjVjNTQxYTI4OTllODg1NWJlYTkyZjhjEgsSBxC42de_hR0YAZIBIwoKcHJvamVjdF9pZBIVQhM1NzU4MTY3OTQ1MDU1OTA1Mzgy&filename=&opi=89354086"
    },
    {
        "name": "China",
        "img_url": "https://lh3.googleusercontent.com/aida/ADBb0uhYG-cfsYJ1zpr911Y51_27fQIZ-ZVKPfA_QPFqFFpQwjQSEcFBnn2SCs85iLjJhiRdHOa6ZeJdXSkgacFHWzuJcvDWLvIvcOPEWkLvrtJAEpdVwT7Hw9TZLl5K47XU6o5xZad5b70g_9VfRJm7bj0TCktLX24exjcu6j12i74TagtJ6755XfHTnGc6BARXclKne2PluYVV4ofaQwpSPIDQv5Ld4InxMXCvA_dj6YyTViEf_NHQpmxnJvA",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzM4ZmMzZjY1ODU0MjQxZjU4ZGIwYWEwMjE5NWMzMDUzEgsSBxC42de_hR0YAZIBIwoKcHJvamVjdF9pZBIVQhM1NzU4MTY3OTQ1MDU1OTA1Mzgy&filename=&opi=89354086"
    },
    {
        "name": "Brazil",
        "img_url": "https://lh3.googleusercontent.com/aida/ADBb0uhA-DU9OS2iuUjgO7efhEci4vl1GekT9oONglZhDe33laD88CJDm-Dy2_M1ybA6hI8aGBaqO3sC8un69WP-logt1ES7Qz7OviA02uhTPwjXCF-wwUqqvOZmIzMKvoJeMqIVKKLsn6lXJmJp993gnuVEkM-1x7OPlTmlY0haocqn6qosMDnwHb7tI9zUU1n8dzaPL6Fn8UpMdp9SRkV485dc6RpG9kU0hcDq6y5BSGSlI3MxymcxuQF-IA",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzQwYzRhZTcwYjYyYjQwZGVhMTM0MzFmZGI4NGNjZjdlEgsSBxC42de_hR0YAZIBIwoKcHJvamVjdF9pZBIVQhM1NzU4MTY3OTQ1MDU1OTA1Mzgy&filename=&opi=89354086"
    },
    {
        "name": "Germany",
        "img_url": "https://lh3.googleusercontent.com/aida/ADBb0ui1UXMz5sw8HJ6A4QrKyVasJOf_nGidyroZlJlujZ9i2rjwITo0MXH9NMwrqU5bGU5JE5XxDA9czmy_n4o7rOnYVjfpX3ruCCohg88MU3SYaKElG3nu2WkVsVnWXXRsQ4ml-xQIVA62k5LUoz0ZkJA9XRSy4U-GnjJp4R2Tsw9GuVkyL2C_sGfpK3bwHwmsyyXw7BO3c7Sz93vWfK4dkgYVgUA5adInr3xAf4Fnp_xQXrStjuDFFGgRUhA",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2M1YzE4YjY0NzZmMzQ3YzFhY2QxOTY4NTNhNWQ0YzU4EgsSBxC42de_hR0YAZIBIwoKcHJvamVjdF9pZBIVQhM1NzU4MTY3OTQ1MDU1OTA1Mzgy&filename=&opi=89354086"
    },
    {
        "name": "Colombia",
        "img_url": "https://lh3.googleusercontent.com/aida/ADBb0ujyJpLJx6d04fKgdOm_ayw2UOcRudoMlRHIiNhn8JtkEsyhjzC-XE10uw8c7MMYHGlWArfdkzp8UpG338_kKT4B9siurOYJaO_YK8wePR3CaeIb5yzd_ZYHF5itVlTMuDHUVvj1NgpHhV9ZGR84kouHrCt2npp-Tx_yhtEAmWuU1GDf87xwBHaJf8fVvFm1hlG87E-OQIbDleySlVQbRhx8jne-eYzgj_4ejFd8o0ycbbvvUwxMIXxqcw",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzkxODJlY2QxMTg4YTQyZTc5YjZjNWNjNTY1YmRhYWIyEgsSBxC42de_hR0YAZIBIwoKcHJvamVjdF9pZBIVQhM1NzU4MTY3OTQ1MDU1OTA1Mzgy&filename=&opi=89354086"
    },
    {
        "name": "USA",
        "img_url": "https://lh3.googleusercontent.com/aida/ADBb0uhLTf9ICXdCzOGAqe6scujiJQTlSoh6WLTaWNh1ZX-YmLtWOdRYNECJwYTzPiiszHinO6b2XFtXOG18S0GfWeyy8F38nSuOAyd3vuOuL9jhgjq8cldZ3qxRRxZtrITA3_c4LUIO3XdL-YyW3sTPezlWFV01lpks0sJ-__mCfCMmtpxV0vUvMEfY23UURkgWY7j2JBXG6A8rD442DBOSP9T2hkdju2U3iJT_lFPf_2bYBeyey_PpJnKvMa8",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2ViZmY5MmJmNmZjYTRlNWJiZGNjYTljODUxOTk0MjgwEgsSBxC42de_hR0YAZIBIwoKcHJvamVjdF9pZBIVQhM1NzU4MTY3OTQ1MDU1OTA1Mzgy&filename=&opi=89354086"
    },
    {
        "name": "Home",
        "img_url": "https://lh3.googleusercontent.com/aida/ADBb0ugO4OPxxXHf90nSh-UaQMVBaaSh2xDpjpbIvd8DCN1bq4c77H1Wjw3WSb3xx-f7GLgLspCKWhDdM2iUeFEUawQEkWuxfyf4p1K56dkvFne-NHX_3XLSJ-I3Ho4AHgGRjOBc3nbtCJwtHA7VfOXfPxr7uEp2DkWlL-AGAdyHrSRlehybMIdaVcjXvOirYVEWFKNIbJJLDc3Xj01RrpbXu46DxGxkaHGlvRgnWfv6FhAG-f91oAO6GzUyyc0",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzlkMDk5NzExOTc5ZTRlOTJiNmE2N2ZjYWMyMzk1ZjYyEgsSBxC42de_hR0YAZIBIwoKcHJvamVjdF9pZBIVQhM1NzU4MTY3OTQ1MDU1OTA1Mzgy&filename=&opi=89354086"
    }
]

out_dir = "screens"
os.makedirs(out_dir, exist_ok=True)

for screen in screens:
    name = screen["name"]
    print(f"Downloading {name}...")
    
    img_path = os.path.join(out_dir, f"{name}.png")
    html_path = os.path.join(out_dir, f"{name}.html")
    
    req_img = urllib.request.Request(screen["img_url"], headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_img) as response, open(img_path, 'wb') as out_file:
        out_file.write(response.read())
        
    req_html = urllib.request.Request(screen["html_url"], headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_html) as response, open(html_path, 'wb') as out_file:
        out_file.write(response.read())

print("Done.")
