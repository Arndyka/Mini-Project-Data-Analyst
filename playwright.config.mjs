import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'tests/browser',workers:2,use:{baseURL:'http://127.0.0.1:4190',channel:process.env.CI?undefined:'msedge'},webServer:{command:'python -m http.server 4190 --bind 127.0.0.1 --directory site',url:'http://127.0.0.1:4190',reuseExistingServer:false},reporter:'list'});
