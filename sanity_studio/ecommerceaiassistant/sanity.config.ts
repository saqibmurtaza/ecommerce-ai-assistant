// sanity.config.ts
import { defineConfig } from 'sanity'
import { visionTool } from '@sanity/vision'
import { schemaTypes } from './schemaTypes'
import {structureTool} from 'sanity/structure'

export default defineConfig({
  name: 'default',
  title: 'ecommerce_ai_assistant',
  projectId: '73s6ouc3',
  dataset: 'production',
  plugins: [
    structureTool(), // <<< Correct v3 plugin usage
    visionTool()
  ],
  schema: {
    types: schemaTypes,
  },
})
