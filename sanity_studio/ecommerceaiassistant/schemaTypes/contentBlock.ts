// // // sanity_studio/ecommerceaiassistant/schemaTypes/contentBlock.ts

// // import { Rule } from '@sanity/types';

// // // Define an interface for the props passed to the prepare function
// // interface ContentBlockPreviewProps {
// //   title: string;
// //   subtitle?: string;
// //   media?: any; // Represents the image asset from Sanity
// //   imageLeft?: boolean;
// //   order: number;
// // }

// // export default {
// //   name: 'contentBlock',
// //   title: 'Content Block (Homepage)',
// //   type: 'document',
// //   fields: [
// //     {
// //       name: 'title',
// //       title: 'Title',
// //       type: 'string',
// //       validation: (Rule: Rule) => Rule.required(),
// //     },
// //     {
// //       name: 'subtitle',
// //       title: 'Subtitle (Optional)',
// //       type: 'string',
// //       description: 'A shorter heading that appears above the main title.',
// //     },
// //     {
// //       name: 'description',
// //       title: 'Description',
// //       type: 'array', // Portable Text for rich content
// //       of: [
// //         {
// //           type: 'block',
// //           styles: [
// //             { title: 'Normal', value: 'normal' },
// //             { title: 'H1', value: 'h1' },
// //             { title: 'H2', value: 'h2' },
// //             { title: 'H3', value: 'h3' },
// //             { title: 'H4', value: 'h4' },
// //           ],
// //           lists: [{ title: 'Bullet', value: 'bullet' }, { title: 'Numbered', value: 'number' }],
// //           marks: {
// //             decorators: [{ title: 'Strong', value: 'strong' }, { title: 'Emphasis', value: 'em' }],
// //             annotations: [
// //               {
// //                 name: 'link',
// //                 type: 'object',
// //                 title: 'Link',
// //                 fields: [
// //                   {
// //                     name: 'href',
// //                     type: 'url',
// //                     title: 'URL',
// //                   },
// //                 ],
// //               },
// //             ],
// //           },
// //         },
// //       ],
// //     },
// //     {
// //       name: 'image',
// //       title: 'Image',
// //       type: 'image',
// //       options: {
// //         hotspot: true,
// //       },
// //       fields: [
// //         {
// //           name: 'alt',
// //           type: 'string',
// //           title: 'Alternative text',
// //           description: 'Important for SEO and accessibility.',
// //         },
// //       ],
// //     },
// //     {
// //       name: 'imageLeft',
// //       title: 'Image on Left?',
// //       type: 'boolean',
// //       initialValue: true,
// //       description: 'If checked, image appears on left; otherwise, image on right.',
// //     },
// //     {
// //       name: 'callToActionText',
// //       title: 'Call to Action Button Text (Optional)',
// //       type: 'string',
// //     },
// //     {
// //       name: 'callToActionUrl',
// //       title: 'Call to Action URL (Optional)',
// //       type: 'url',
// //     },
// //     {
// //       name: 'order',
// //       title: 'Order',
// //       type: 'number',
// //       description: 'Determines the display order of sections on the homepage.',
// //       validation: (Rule: Rule) => Rule.required().integer().min(0),
// //     },
// //   ],
// //   preview: {
// //     select: {
// //       title: 'title',
// //       subtitle: 'subtitle',
// //       media: 'image', // 'media' is standard for preview image
// //       imageLeft: 'imageLeft',
// //       order: 'order',
// //     },
// //     // Type the destructured parameters
// //     prepare({ title, subtitle, media, imageLeft, order }: ContentBlockPreviewProps) {
// //       const layoutText = imageLeft ? 'Image Left' : 'Image Right';
// //       return {
// //         title: `${order}. ${title}`,
// //         subtitle: `${subtitle || ''} [Layout: ${layoutText}]`,
// //         media,
// //       };
// //     },
// //   },
// // };


// // sanity_studio/ecommerceaiassistant/schemaTypes/contentBlock.ts

// // Remove 'import { Rule } from '@sanity/types';'
// // Instead, import defineType and defineField directly from 'sanity'
// import { defineType, defineField, PreviewValue, PrepareViewOptions } from 'sanity';

// // Define an interface for the props passed to the prepare function (still useful for clarity)
// interface ContentBlockPreviewProps {
//   title: string;
//   subtitle?: string;
//   media?: any; // Represents the image asset from Sanity
//   imageLeft?: boolean;
//   order: number;
// }

// export default defineType({
//   name: 'contentBlock',
//   title: 'Content Block (Homepage)',
//   type: 'document',
//   fields: [
//     defineField({
//       name: 'title',
//       title: 'Title',
//       type: 'string',
//       // Remove ': Rule' from the parameter type, let TypeScript infer it
//       validation: (Rule) => Rule.required(),
//     }),
//     defineField({
//       name: 'subtitle',
//       title: 'Subtitle (Optional)',
//       type: 'string',
//       description: 'A shorter heading that appears above the main title.',
//     }),
//     defineField({
//       name: 'description',
//       title: 'Description',
//       type: 'array',
//       of: [
//         {
//           type: 'block',
//           styles: [
//             { title: 'Normal', value: 'normal' },
//             { title: 'H1', value: 'h1' },
//             { title: 'H2', value: 'h2' },
//             { title: 'H3', value: 'h3' },
//             { title: 'H4', value: 'h4' },
//           ],
//           lists: [{ title: 'Bullet', value: 'bullet' }, { title: 'Numbered', value: 'number' }],
//           marks: {
//             decorators: [{ title: 'Strong', value: 'strong' }, { title: 'Emphasis', value: 'em' }],
//             annotations: [
//               {
//                 name: 'link',
//                 type: 'object',
//                 title: 'Link',
//                 fields: [
//                   {
//                     name: 'href',
//                     type: 'url',
//                     title: 'URL',
//                   },
//                 ],
//               },
//             ],
//           },
//         },
//       ],
//     }),
//     defineField({
//       name: 'image',
//       title: 'Image',
//       type: 'image',
//       options: {
//         hotspot: true,
//       },
//       fields: [
//         defineField({
//           name: 'alt',
//           title: 'Alternative text',
//           type: 'string', // Ensure type is here
//           description: 'Important for SEO and accessibility.',
//         }),
//       ],
//     }),
//     defineField({
//       name: 'imageLeft',
//       title: 'Image on Left?',
//       type: 'boolean',
//       initialValue: true,
//       description: 'If checked, image appears on left; otherwise, image on right.',
//     }),
//     defineField({
//       name: 'callToActionText',
//       title: 'Call to Action Button Text (Optional)',
//       type: 'string',
//     }),
//     defineField({
//       name: 'callToActionUrl',
//       title: 'Call to Action URL (Optional)',
//       type: 'url',
//     }),
//     defineField({
//       name: 'order',
//       title: 'Order',
//       type: 'number',
//       description: 'Determines the display order of sections on the homepage.',
//       // Remove ': Rule' from the parameter type, let TypeScript infer it
//       validation: (Rule) => Rule.required().integer().min(0),
//     }),
//   ],
//   preview: {
//     select: {
//       title: 'title',
//       subtitle: 'subtitle',
//       media: 'image',
//       imageLeft: 'imageLeft',
//       order: 'order',
//     },
//     prepare(value: Record<string, any>, viewOptions?: PrepareViewOptions): PreviewValue {
//       const { title, subtitle, media, imageLeft, order } = value;
//       const layoutText = imageLeft ? 'Image Left' : 'Image Right';
//       return {
//         title: `${order}. ${title}`,
//         subtitle: `${subtitle || ''} [Layout: ${layoutText}]`,
//         media: media,
//       };
//     },
//   },
// });

// sanity_studio/ecommerceaiassistant/schemaTypes/contentBlock.ts

import { defineType, defineField, PreviewValue, PrepareViewOptions } from 'sanity';

export default defineType({
  name: 'contentBlock',
  title: 'Content Block (Homepage)',
  type: 'document',
  fields: [
    defineField({ // Use defineField for each field
      name: 'title',
      title: 'Title',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
    defineField({ name: 'subtitle', title: 'Subtitle (Optional)', type: 'string', description: 'A shorter heading that appears above the main title.' }),
    defineField({ name: 'description', title: 'Description', type: 'array', of: [{ type: 'block', styles: [{ title: 'Normal', value: 'normal' }], marks: { decorators: [{ title: 'Strong', value: 'strong' }], annotations: [{ name: 'link', type: 'object', title: 'Link', fields: [{ name: 'href', type: 'url', title: 'URL' }] }] } }] }),
    defineField({
      name: 'image',
      title: 'Image',
      type: 'image',
      options: { hotspot: true },
      fields: [defineField({ name: 'alt', title: 'Alternative text', type: 'string', description: 'Important for SEO and accessibility.' })],
    }),
    defineField({ name: 'imageLeft', title: 'Image on Left?', type: 'boolean', initialValue: true, description: 'If checked, image appears on left; otherwise, image on right.' }),
    defineField({ name: 'callToActionText', title: 'Call to Action Button Text (Optional)', type: 'string' }),
    defineField({ name: 'callToActionUrl', title: 'Call to Action URL (Optional)', type: 'url' }),
    defineField({
      name: 'order',
      title: 'Order',
      type: 'number',
      description: 'Determines the display order of sections on the homepage.',
      validation: (Rule) => Rule.required().integer().min(0),
    }),
  ],
  preview: {
    select: {
      title: 'title',
      subtitle: 'subtitle',
      media: 'image',
      imageLeft: 'imageLeft',
      order: 'order',
    },
    // <<<<<<<<<<<< CRITICAL FIX IS HERE >>>>>>>>>>>>>
    // Accept a single 'value' parameter, then destructure inside.
    prepare(value: Record<string, any>, viewOptions?: PrepareViewOptions): PreviewValue {
      const { title, subtitle, media, imageLeft, order } = value; // <<<< DESTRUCTURE HERE
      const layoutText = imageLeft ? 'Image Left' : 'Image Right';
      return {
        title: `${order}. ${title}`,
        subtitle: `${subtitle || ''} [Layout: ${layoutText}]`,
        media: media,
      };
    },
  },
});
