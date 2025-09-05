import pillow1 from "../../assets/pillow1.webp";
import pillow2 from "../../assets/pillow2.webp";
import pillow3 from "../../assets/pillow3.webp";
import pillow4 from "../../assets/pillow4.webp";
import pillow5 from "../../assets/pillow5.webp";
import pillow6 from "../../assets/pillow6.webp";
import pillow7 from "../../assets/pillow7.webp";
import pillow8 from "../../assets/pillow8.webp";
import pillow9 from "../../assets/pillow9.webp";
import pillow10 from "../../assets/pillow1.webp";
import pillow11 from "../../assets/pillow2.webp";
import pillow12 from "../../assets/pillow3.webp";
import pillow13 from "../../assets/pillow4.webp";
import pillow14 from "../../assets/pillow5.webp";
import pillow15 from "../../assets/pillow6.webp";
import pillow16 from "../../assets/pillow7.webp";
import pillow17 from "../../assets/pillow8.webp";
import pillow18 from "../../assets/pillow9.webp";
import pillow19 from "../../assets/pillow2.webp";
import pillow20 from "../../assets/pillow3.webp";
import pillow21 from "../../assets/pillow4.webp";
import pillow22 from "../../assets/pillow5.webp";
import pillow23 from "../../assets/pillow6.webp";
import pillow24 from "../../assets/pillow7.webp";
const pillowsData = [
  {
    id: 1,
    name: "Molty Gold Pillow",
    price: "Rs.1,800",
    img: pillow1,
    description: "A mattress for your head, Molty Gold pillow provides firm support for a good night's sleep and lets you sleep like a baby. The Anti-Microbial Protection is perfect for people with allergies and breathing disorders."
  },
  {
    id: 2,
    name: "MoltyOrtho Knee Pillow",
    price: "Rs.1,935",
    img: pillow2,
    description: "MoltyOrtho  Knee Pillow for sleeping provides maximum support and pressure relief on the lower back, spine and hip pain. The pillow is designed to alleviate joint pains and the rubbing of the knees. It also helps reduce back pain and provides adequate alignment to reduce Sciatica."
  },
  {
    id: 3,
    name: "MoltyMom Pregnancy Wedge",
    price: "Rs.2,000",
    img: pillow3,
    description: "MoltyMom pregnancy wedge is specifically designed to offer proper support and reduce the swelling in hands, legs, and feet by relieving back tension and associated stress."
  },
    {
    id: 4,
    name: "MoltyBaby Wedge Pillow",
    price: "Rs.2,150",
    img: pillow4,
    description: "MoltyBaby wedge pillow offers the supportive incline needed to raise your baby's head and torso by the perfect degree. This can keep some of the stomach acids from causing discomfort or spitting up overnight, which helps both the baby and the parents sleep better."
  },
  {
    id: 5,
    name: "Molty Pillow",
    price: "Rs.2,550",
    img: pillow5,
    description: "Sleep Tight, rise Bright! Indulge in a restful slumber with Molty Pillow. Crafted with a unique blend of quality micro and ball fiber, this best bed pillow provide medium support for your neck. Each pillow is lovingly filled with only the finest fibers which provide a squishy and cozy pillow to help you sink into the most blissful night's sleep."
  },
    {
    id: 6,
    name: "MoltyMom Pregnancy Support",
    price: "Rs.3,000",
    img: pillow6,
    description: "Experience unmatched softness with our Luxe Comfort Pillow, designed for ultimate neck support and restful sleep."
  },
  {
    id: 7,
    name: "Memory Baby Head Shaper Pillow",
    price: "Rs.3,400",
    img: pillow7,
    description: "Baby Head-Shaping Pillow is comprised of a unique design and quality high-density foam that provides great support to the baby’s head. The special cut-out design provides room for an infant’s head, supports the head movement, offers air regulation, and prevents the baby from “Flat Head Syndrome”"
  },
    {
    id: 8,
    name: "Celeste Microfiber Pillow",
    price: "Rs.3,600",
    img: pillow8,
    description: "Celeste pillow is unbelievably lightweight and plush. It's ultra soft texture provides the ideal balance of cushiness and support; improving your sleep experience altogether."
  },
  {
    id: 9,
    name: "Celeste Dream Pillow",
    price: "Rs.4,000",
    img: pillow9,
    description: "Designed to cradle your head in a blissful and restorative sleep, this pillow is crafted with a premium blend of microfiber filling that offers a naturally bouncy feel."
  },
    {
    id: 10,
    name: "Celeste Hotel Pillow",
    price: "Rs.4,100",
    img: pillow10,
    description: "Celeste Luxury Hotel Pillow is meticulously manufactured, keeping in view your desire to enjoy a hotel-like feeling. The specialty of this hotel pillow is its luxurious feel, which balances plushness and support."
  },
  {
    id: 11,
    name: "Contour Pillow",
    price: "Rs.4,230",
    img: pillow11,
    description: "Contour Pillow is designed with massaging grooves for relaxation. Designed to support the contours of your neck and body for an appropriate posture for a restful sleep."
  },
  {
    id: 12,
    name: "MoltyFoam Duo Comfort Pillow",
    price: "Rs.4,500",
    img: pillow12,
    description: "Introducing our revolutionary new pillow, crafted to deliver the ultimate sleep experience - the perfect fusion of foam and fiber. Designed with meticulous attention to detail, our pillow strikes an impeccable balance between unmatched comfort and exceptional support."
  },
    {
    id: 13,
    name: "Every mother’s best friend, MoltyBaby Nursing pillow perfectly offers versatile support for the baby’s feeding time. The versatile nursing pillow by SoFoam lifts the baby to a more ergonomic position for comfortable feeding, then transitions to the perfect spot for propping, tummy time, and learning to sit.",
    price: "Rs.4,500",
    img: pillow13,
    description: "Experience unmatched softness with our Luxe Comfort Pillow, designed for ultimate neck support and restful sleep."
  },
  {
    id: 14,
    name: "MoltyOrtho Turnover Pillow",
    price: "Rs.4,815",
    img: pillow14,
    description: "This thoughtfully designed U-shaped pillow with arc design helps the bedridden and elderly patients turn over without any discomfort. Helping patients to easily change their body posture and prevent bedsores, this pillow provides comfortable support since it is easy to use."
  },
    {
    id: 15,
    name: "MoltyCure Wedge",
    price: "Rs.5,350",
    img: pillow15,
    description: "The MoltyCure Wedge Pillow provides the perfect support to elevate your upper body, legs, or to use as a trunk stabilizer for lying on your side. This high quality product is designed for pregnant women and those suffering from acid reflux, difficulty breathing, poor circulation, hiatal hernias, back, or neck problems. Can be used to elevate your feet or legs as well. "
  },
  {
    id: 16,
    name: "MoltyMom Pregnancy Pillow Total Body",
    price: "Rs.7,000",
    img: pillow16,
    description: "Looking for a perfect pillow for side sleeping during pregnancy? MoltyMom Pregnancy Pillow Total Body is carefully crafted to substitute the need for regular pillows while providing more proficient support."
  },
    {
    id: 17,
    name: "Triangular Wedge Pillow",
    price: "Rs.7,500",
    img: pillow17,
    description: "Triangular Wedge Pillow is ergonomically designed to support the natural curvature of the back and provide optimal elevation for the upper body. This pillow can be used as a back support, to fill gap between the headboard/wall and your mattress, or simply as a fashionable home decoration - ensuring maximum comfort while sitting reading and watching TV!'"
  },
  {
    id: 18,
    name: "MoltyOrtho Memory Cervical",
    price: "Rs.10,350",
    img: pillow18,
    description: "The MoltyOrtho Memory Cervical Pillow is designed specifically for patients with neck and cervical issues. It helps you sleep better by providing a firm authentic support and enables better sleep, for a healthier you."
  },
      {
    id: 19,
    name: "MoltyOrtho Memory Pillow",
    price: "Rs.10,350",
    img: pillow19,
    description: "Experience unmatched softness with our Luxe Comfort Pillow, designed for ultimate neck support and restful sleep."
  },
  {
    id: 20,
    name: "Hexa Cool Pillow",
    price: "Rs.15,000",
    img: pillow20,
    description: "Experience the ultimate in cooling comfort with the Hexa Cool Pillow. Designed with an innovative Hex-Mesh Technology and Cool AirFlow System, this pillow ensures continuous ventilation, keeping you cool and refreshed all night long. Its ergonomic structure offers superior neck and head support, promoting a restful, pressure-free sleep."
  },
      {
    id: 21,
    name: "Cool Gel Pillow",
    price: "Rs.16,000",
    img: pillow21,
    description: "Molty Cool Gel Pillow will assure you comfort and relief like no other. By cutting down body heat to almost 5 degrees this pillow guarantees the “cold-side-of-the-pillow” feeling all night long."
  },
  {
    id: 22,
    name: "Latex Pillow",
    price: "Rs.20,000",
    img: pillow22,
    description: "The Latex Pillow is particularly designed to offer uplifting support to your neck and bottomless pressure relief for your head. You will feel your head and neck being cradled as the pillow conforms to you, giving you a more buoyant feel. Owing to its durability, breathability, and advanced comfort, you will have the sleep of your dreams!"
  },
      {
    id: 23,
    name: "Duck Down Feather Pillow",
    price: "Rs.25,000",
    img: pillow23,
    description: "Synonymous with ultimate plushness and cloudy comfort, our premium Duck Down Feather Pillow provides the perfect balance of relaxation and support for a blissful night’s sleep. Luxuriously woven and encased in 100% Cotton Fabric with 50% Duck Down and 50% Feather, and an extra inner layering for insulation."
  },
  {
    id: 24,
    name: "Aloe Vera Memory Pillow",
    price: "Rs.25,000",
    img: pillow24,
    description: "The Aloe Vera memory foam technology comes with a thermoregulator that senses temperature changes and creates a cooling effect when it’s warm and absorbs excess heat on hotter days. It also contains healing properties of Aloe Vera which are both, healthy and soothing."
  }
];

const accessoriesData = [
  {
    name: "MoltyFoam Portable Jai Namaz",
    price: "Rs.4,050",
    description: "Our portable Jai Namaz is easy to roll and carry around while traveling. Completely convenient to store, it features non-slip material on the back, so you can pray comfortably without slipping. Its material makes the surface very soft, which help you make soujoud longer without any strain on the forehead and knees. Its padded surface provides a high level of comfort and support to your knees during prayer. This portable Islamic prayer rug is soft enough on hard, carpeted, and wood floors alike. It is easy to carry owing to its unique design and durable structure. Perfect for daily use, it is made to last for years to come."
  },
  {
    name: "Deluxe Jai Namaz",
    price: "Rs.5,000",
    description: "MoltyFoam Jai Namaz is crafted with a 'Velvet Fabric' top and high-density foam. It offers comfortable knee support while you are praying and kneeling. The 'Acrylic Felt' absorbs pressure while the 'Anti-skid Fabric' at the bottom keeps you from slipping.-Lightweight and Durable-HD Foam Technology-Soft & Comfortable-Best Knee Support"
  },
   {
    name: "MoltyOrtho Back Care Cushion",
    price: "Rs.4,300Rs.3,870",
    description: "The MoltyOrtho Back Care Cushion prevents backache while one is driving or is at work."
  },
  {
    name: "Celeste Jai Namaz",
    price: "priceRs.7,500",
    description: "The Celeste Memory Jai Namaz is thoughtfully designed to enhance your prayer experience with comfort and support. Made with high-resilience memory foam, it cushions pressure points especially the knees and ankles during sujood and tashahhud, reducing fatigue and strain.-Memory Foam-Velvet Luxe Surface-Anti-Skid Stability-Compact and Elegant Portability"
  },
    {
    name: "MoltyFoam Jai Namaz",
    price: "Rs.4,050Rs.4,000",
    description: "Plush Velvet Jai Namaz quilted with high density rebounded foam and matching fabric underlining provide ease of offering prayer and protects knees of the elderly."
  },
     {
    name: "MoltyOrtho Cool Memory Coccyx",
    price: "Rs.8,700",
    description: "MoltyOrtho Cool Memory Coccyx Cushion is an ultimate blend of Orthopedic support and cooling comfort. Designed with high-density memory foam and an advanced cooling gel layer, it alleviates pressure on your lower spine, promotes healthy posture, and keeps you comfortably cool during long hours of sitting. Whether at work, in your car, or at home, experience superior support where you need it most."
  },
  {
    name: "Coccyx Cushion",
    price: "Rs.4,800Rs.4,320",
    description: "The unique cut out design is what sets our Molty Foam Coccyx Care Cushion apart. It suspends the coccyx and eliminates all the pressure from the back while sitting or driving, (especially on sensitive areas like tail bone)."
  },
    {
    name: "Ultra Water Proof Protector",
    price: "Rs.7,100",
    description: "Molty ultra waterproof mattress protector is made using the highest quality hypo allergenic materials. It protects your mattress from expensive spills while protecting your family from allergens and dust mites lurking in your mattress. It is carefully designed to lock in moisture for the best protection and comfort available."
  },
  {
    name: "Lumbar Support Cushion",
    price: "Rs.7,950Rs.7,155",
    description: "The perfect ergonomic structure of MoltyOrtho Lumbar support is designed to provide relief from upper, mid, and low back pain due to driving, long working hours, and some injury. Besides providing extreme contour cushioning, the high-end memory foam also absorbs jerks and shocks while driving to prevent muscle spasms and backaches. The ideal size of the cushion makes it a great portable solution for work and travelling."
  },
 {
    name: "MoltyOrtho Knee Pillow",
    price: "Rs.2,150Rs.1,935",
    description: "MoltyOrtho by moltyfoam is the full range of Medically approved sleeping accessories.MoltyOrtho  Knee Pillow for sleeping provides maximum support and pressure relief on the lower back, spine and hip pain. The pillow is designed to alleviate joint pains and the rubbing of the knees. It also helps reduce back pain and provides adequate alignment to reduce Sciatica."
  },
   {
    name: "Ring Cushion",
    price: "Rs.4,800Rs.4,320",
    description: "Designed ideally for patients with piles, the ring cushion distributes body weight evenly without putting pressure on the lower abdomen. It provides effective pain relief and healing of the affected area. The cover is hypoallergenic and machine washable to maintain hygiene at all times."
  },
    {
    name: "MoltyOrtho Topper",
    price: "Rs.7,500Rs.6,750",
    description: "MoltyOrtho Topper is a quick and affordable solution to your uncomfortable mattress problems. The convoluted zones help alleviate painful pressure points by distributing body weight and provide a firm sleeping surface to your existing mattress that helps reduce pain and align the spine."
  },
   {
    name: "MoltyOrtho HeadRest Cushion",
    price: "Rs.4,800Rs.4,320",
    description: "MoltyOrtho Headrest provides additional support for your neck, cervical and head and helps improve posture while traveling, reducing muscle tension and stress. Made from high-quality memory foam, it molds to your neck and head perfectly to give you just the right amount of cushion for extra comfort."
  },
     {
    name: "Mattress Protector",
    price: "Rs.4,600",
    description: "Molty Protector is made using the highest quality hypo allergenic materials. It protects and resists dust mites from lurking in your mattress. The fresh guard technology prevents your family from allergens. The protector is carefully designed for best protection and offers a comfortable sleeping experience"
  },
     {
    name: "Celeste Sherpa Quilt",
    price: "Rs.10,800",
    description: "Experience the ultimate in cozy comfort with the Celeste Sherpa Quilt. Designed to provide superior warmth, this blanket combines the luxurious softness of Sherpa fleece with a stylish quilted design for a perfect night's sleep."
  },
  {
    name: "Molty Razai Winter Quilt",
    price: "Rs.6,000",
    description: "Molty Razai is made with microfiber cover and fill and is incredibly lightweight, soft, fluffy, and warm. The baffle box construction keeps filling from moving around, so it provides an even layer of warmth. Moreover, the hypoallergenic fill is healthier for anyone who suffers from allergies"
  },
    {
    name: "Cervical Collar",
    price: "Rs.4,700Rs.4,230",
    description: "MoltyFoam Cervical Collar fits the neck comfortably and helps release pain and accelerate tissue recovery by keeping them warm. It is multi-purpose, can be used during flight, computer work, reading, watching TV and stabilize neck while sleeping."
  },
   {
    name: "Relaxor Cushion",
    price: "Rs.3,500",
    description:"Lack back support watching television or reading your favorite book? Molty Relaxor Cushion is your best pick. Providing you the ultimate support, it gets you the comfort you have always been looking for."
  },
  {
    name: "Mattress Storage Bag",
    price: "Rs.550",
    description:"For all of your moving or transportation needs, here is a convenient and durable nonwoven mattress cover that comes with a zipper. It completely surrounds your mattress for protection while moving or placing it into storage.- A protective solution for long-term mattress storage or short-term transportation- Dimensional shape designed specifically to fit any size of mattress- Keeps out dust, pests, odors, and moisture- Slips over the mattress like a pillowcase and gets sealed with a zipper"
  },
  {
    name: "MoltyFoam Car Seat Head Cushion",
    price: "Rs.3,650",
    description:"Looking for the perfect car seat head cushion that offers you the best support while driving car for long hours? Equipped with an elasticated strap and zipper on the back, the MoltyFoam Head Cushion is the best for you! This polyester cushion provides strong support for your cervical spine and head, helps you maintain the correct posture in the car seat or office seat, and absorbs jolts from rough road conditions, including potholes, uneven pavement, and off-roading conditions. It effectively relieves back and waist pain, numbness, and tension during driving and sitting for a long time. (2 Units Inside the Box)"
  },
  {
    name: "Relaxor - Knitted Fabric",
    price: "Rs.4,400",
    description:"Relax better than ever!The all new Molty Relaxor cushion provides the ideal support your back needs. The beautifully knitted fabric and the soft plush feel allows easy reading or studying. The ball fiber filling fluffs add up to allow a cozy, relaxing feel to ensure maximum comfort."
  },
  {
    name: "MoltyOrtho Back Support Topper",
    price: "Rs.13,950",
    description:"MoltyOrtho Back Support Topper is engineered to relieve pressure and provide the best ergonomic support. The topper helps distribute the weight evenly and lifts pressure off of your bones. It preserves your posture while sleeping & provide balanced support all night long."
  },
  {
    name: "MoltyOrtho D-Shape Pillow",
    price: "Rs.4,410",
    description:"Seeking a supportive aid that cradles your body in the best position to maintain a straight spine? MoltyOrtho D-Shape Pillow is here to put an end to your quest! It helps relieve the debilitating effects of sciatica, arthritis, back pain, and post-surgery pain, helps the vertebrae stay relaxed, keeps the neck & shoulders aligned, and maintains the spine’s natural curvature.100% highly resilient foam with optimized firmness provides proper support for the lower back region to relieve the pain from muscle pressure, tension, and strain caused by prolonged poor posture. It provides long-lasting comfort for hours. Superior to other roll pillows, it won't go flat over time and provides optimal support and spinal alignment"
  },
  {
    name: "MoltyOrtho Bolster Pillow",
    price: "Rs.5,400",
    description:"This ergonomic bolster shape pillow helps reduce head, shoulder, neck, and back discomfort. Simply place it under the problem areas for instant pain relief. Made with premium quality HD foam, the MoltyOrtho Bolster pillow supports an ideal spine alignment. It surely is a must-have for physiotherapy sessions for the best results"
  },
  {
    name: "MoltyOrtho Duo Topper",
    price: "Rs.13,950",
    description:"MoltyOrtho Duo Topper is designed with the “His & Her Mattress” approach. The high-performance corrugated surface delivers the perks of firm support with one half and an orthopedic firm surface with the other half. It is specifically designed to meet the unique needs of two individuals!"
  },
  {
    name: "Weighted Blanket",
    price: "Rs.17,300",
    description:"Soft pressure from our weighted blanket induces a calming effect in the body and helps you fall asleep. Designed to help reduce anxiety by stimulating the sensation of being hugged and producing feel-good hormones, like Serotonin, to make you feel comforted and relaxed. The gentle pressure applied by the blanket may help insomnia sufferers by enabling them to have a deeper and better night’s sleep. Allow yourself to unwind, and reduce tension thus boosting a naturally restful sleep."
  },
  {
    name: "Celeste Fitted Bed Sheet (3 Piece)",
    price: "Rs.7,500",
    description:"Upgrade your bedding experience with our Fitted Sheet and 2 Pillow Covers Set, combining functionality and sophistication in one package. Our fitted sheet is expertly crafted from premium, high-quality fabric to provide you with the ultimate sleeping surface. Its fitted design ensures a snug and secure fit over your mattress, keeping it in place throughout the night. Its deep pockets accommodate even the thickest mattresses, providing a seamless fit and preventing any annoying bunching or slipping."
  },
  {
    name: "Molty Memory Topper",
    price: "Rs.25,000",
    description:"Our Molty Memory Topper is a winner! It transforms your old mattress into one that will enable you a comfortable sleep. Reducing pressure by contouring and memorizing your body’s natural shape; it provides you right support for a restful slumber. With an unmatched quality, this topper is an ideal choice!"
  },
  {
    name: "Cool Gel 7 Zone Topper",
    price: "Rs.12,500",
    description:"Improve the comfort level of your current mattress with the supportive and breathable Molty Cool Gel 7-Zone Mattress Topper. The advanced air flow technology along with infused cool gel enable right support & is the perfect solution for a comfortable, cooler night's sleep."
  },
  {
    name: "Molty Baby Mattress",
    price: "Rs.9,100",
    description:"The MoltyBaby mattress is the best mattress choice for your newborn, infant, or toddler. This premium crib mattress is designed to fit any standard full-size crib and toddler bed. The ideal firmness for infant safety and development, this mattress features a core made of high-quality, breathable foam to maximize air flow and comfort for your little one."
  },
  {
    name: "Memory Cool Gel Travel Pillow",
    price: "Rs.7,950",
    description:"The Memory Cool Gel Pillow resist motion and is great as it molds to your neck shape. The Cool Gel provides a cooler soothing effect continuing to be comfortable regardless how long your journey is."
  },
  {
    name: "MoltyOrtho CoolBackCare",
    price: "Rs.8,550",
    description:"MoltyOrtho CoolBackCare is designed to help correct your posture and prevent, reduce or stop back pain altogether. The cool fabric on the Back Care resists heat, making journeys more comfortable."
  },
  {
    name: "Mattress Pad",
    price: "Rs.7,200",
    description:"Molty Mattress pad is designed to bring a super soft plush finish to your existing mattress. This quilted pad is durable and long lasting and is significant for two main reasons; to keep your mattress free of stains and to prevent exposure to dust mites and other potential allergens."
  },
  {
    name: "Molty Summer Quilt",
    price: "Rs.9,600",
    description:"Our fluffy and light weight summer quilt is excellent at absorbing and moving moisture away from your body. It keeps you warm and give you plush feel. The synthetic fiber allows air to circulate and maintain body temperature."
  },
  {
    name: "Molty Memory Travel Pillow",
    price: "Rs.5,400",
    description:"With the adjustable thickness and conforming properties of memory, MoltyMemory Travel Pillow is easiest to handle during long travels. Its flat ergonomic design takes the shape of the neck and provides perfect support to enjoy restful sleep while traveling."
  },
  {
    name: "Cooling Blanket",
    price: "Rs.11,200",
    description:"The most incredible cooling blanket made just for you by combining state-of-the-art craftsmanship with sumptuous materials. Incredibly soft yet lightweight and compact, the Celeste Cooling blanket can be used for sleeping and lounging. Richly filled with a unique blend of heat-absorbing materials that make it your perfect companion all year round. Absorbing excess heat keeps you cool and sweat-free all night long so you wake up comfortably cool. Have an undisturbed sleep and wake up feeling refreshed."
  },
  {
    name: "MoltyBaby Sleeper",
    price: "Rs.4,500",
    description:"Introducing the MoltyBaby Sleeper - a hassle-free, multi-purpose solution for ensuring your baby has a comfortable and safe surface to lie in. This thoughtfully crafted, easy-to-set up product can double as both a bed and a playmat, providing a safe and cozy environment for your little one. Crafted from firm foam and equipped with fiber side guards, it guarantees your baby stays safely in place without any rolling mishaps.The MoltyBaby Sleeper is fashioned from soft, breathable fabric, that mimics the soothing embrace of a mother's arms, creating a cozy haven for your baby to rest and relax. Its lightweight yet durable design ensures effortless handling and also makes it perfect for use as a portable travel bed."
  },
  {
    name: "MoltyOrtho Massage Bed Foldable",
    price: "Rs.45,450",
    description:"This massage table is a blend of innovation and practicality designed for ultimate relaxation and therapeutic care. Crafted with an artificial leather surface and a durable beechwood leg structure, this massage bed ensures both comfort and longevity. Its adjustable height feature caters to various needs, while its foldable design makes storage and portability a breeze. Equipped with a face cradle and armrests, the bed provides enhanced comfort for every user."
  },
  {
    name: "Master Black Face Masks Box",
    price: "Rs.385",
    description:"Buy Best Quality Surgical Face Mask online in bulk quantity in Pakistan. To filter and protect the air you are breathing in Master Nonwoven manufactures quality face masks. High quality spun-bonded nonwoven fabric helps in filtering the dust particles, bacteria, viruses, and other infectious materials from the air you are inhaling and prevent you from several health problems. The masks are created with great precision to provide a health-friendly and comfortable user experience. Master Nonwoven’s special 3 layered masks fit well to every face providing several customization options so that users can adjust it according to their needs."
  },
  {
    name: "Master Blue Face Masks Box",
    price: "Rs.250",
    description:"To filter and protect the air you are breathing in Master Nonwoven manufactures quality face masks. High quality spun-bonded nonwoven fabric helps in filtering the dust particles, bacteria, viruses, and other infectious materials from the air you are inhaling and prevent you from several health problems. The masks are created with great precision to provide a health-friendly and comfortable user experience. Master Nonwoven’s special 3 layered masks fit well to every face providing several customization options so that users can adjust it according to their needs."
  }
];

// Export everything together
const allProducts = {
  pillows: pillowsData,
  accessories: accessoriesData
};

export default allProducts;