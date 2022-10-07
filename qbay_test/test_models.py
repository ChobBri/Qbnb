from qbay.models import create_listing, register, login
from qbay.models import update_listing, User, Listing
from datetime import date


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    assert register('u0', 'test0@test.com', '123456') is True
    assert register('u0', 'test1@test.com', '123456') is True
    assert register('u1', 'test0@test.com', '123456') is False


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address
      and the password.
    (will be tested after the previous test, so we already have u0,
      u1 in database)
    '''

    user = login('test0@test.com', 123456)
    assert user is not None
    assert user.username == 'u0'

    user = login('test0@test.com', 1234567)
    assert user is None


def test_r4_1_create_listing():
    '''
    Testing R4-1: The title of the product has to be alphanumeric-only, and
      space allowed only if it is not as prefix and suffix.
    '''
    user = User.query.filter_by().first()

    # Case 1: Empty Title
    listing = create_listing('', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None
    
    # Case 2: Regular Title
    listing = create_listing('The Title', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 3: Regular Title with Numbers
    listing = create_listing('The Title62', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 4: Title with Space as Prefix
    listing = create_listing(' The Title62', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None
    
    # Case 5: Title with Space as Suffix
    listing = create_listing('The Title62 ', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None
    
    # Case 6: Title with Underscore
    listing = create_listing('The Tit_le', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None

    
def test_r4_2_create_listing():
    '''
    Testing R4-2: The title of the product is no longer than 80 characters.
    '''
    user = User.query.filter_by().first()
    
    # Case 1: Title of 1 character
    listing = create_listing('A', 'description of listing',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 2: Title of 80 characters
    listing = create_listing('x' * 80, 'description of listing' + 'x' * 80,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 3: Title of 81 characters
    listing = create_listing('x' * 81, 'description of listing' + 'x' * 81,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None


def test_r4_3_create_listing():
    '''
    Testing R4-3: The description of the product can be arbitrary characters,
      with a minimum length of 20 characters and a maximum of 2000 characters.
    '''
    user = User.query.filter_by().first()
    
    # Case 1: Description of 20 characters
    listing = create_listing('Title1', 'x' * 20,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 2: Description of 2000 characters
    listing = create_listing('Title2', 'x' * 2000,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 3: Description of 19 characters
    listing = create_listing('Title3', 'x' * 19,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None
    
    # Case 4: Description of 2001 characters
    listing = create_listing('Title4', 'x' * 2001,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None
    
    # Case 5: Description of arbitrary characters
    listing = create_listing('Title5', '  abc ABC 123 !@#  _~["',
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None


def test_r4_4_create_listing():
    '''
    Testing R4-4: Description has to be longer than the product's title.
    '''
    user = User.query.filter_by().first()
    
    # Case 1: Description longer than title
    listing = create_listing('x' * 23, 'x' * 25,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 2: Description length equal to title length
    listing = create_listing('y' * 23, 'x' * 23,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None
    
    # Case 3: Description shorter than title
    listing = create_listing('z' * 23, 'x' * 21,
                             30.00, date(2022, 10, 6), user.id)
    assert listing is None


def test_r4_5_create_listing():
    '''
    Testing R4-5: Price has to be of range [10, 10000].
    '''
    user = User.query.filter_by().first()
    
    # Case 1: Price = 10
    listing = create_listing('Title11', 'description of listing',
                             10, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 2: Price = 10000
    listing = create_listing('Title12', 'description of listing',
                             10000, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 3: Price = 50
    listing = create_listing('Title13', 'description of listing',
                             50, date(2022, 10, 6), user.id)
    assert listing is not None
    
    # Case 4: Price = 9.99
    listing = create_listing('Title14', 'description of listing',
                             9.99, date(2022, 10, 6), user.id)
    assert listing is None
    
    # Case 5: Price = 10000.01
    listing = create_listing('Title15', 'description of listing',
                             10000.01, date(2022, 10, 6), user.id)
    assert listing is None


def test_r4_6_create_listing():
    '''
    Testing R4-6: last_modified_date must be after 2021-01-02
      and before 2025-01-02.
    '''
    user = User.query.filter_by().first()
    
    # Case 1: last_modified_date = 2021-01-03
    listing = create_listing('Title21', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is not None
    
    # Case 2: last_modified_date = 2025-01-01
    listing = create_listing('Title22', 'description of listing',
                             30.00, date(2025, 1, 1), user.id)
    assert listing is not None
    
    # Case 3: last_modified_date = 2023-01-01
    listing = create_listing('Title23', 'description of listing',
                             30.00, date(2023, 1, 1), user.id)
    assert listing is not None
    
    # Case 4: last_modified_date = 2021-01-02
    listing = create_listing('Title24', 'description of listing',
                             30.00, date(2021, 1, 2), user.id)
    assert listing is None
    
    # Case 5: last_modified_date = 2025-01-02
    listing = create_listing('Title25', 'description of listing',
                             30.00, date(2025, 1, 2), user.id)
    assert listing is None


def test_r4_7_create_listing():
    '''
    Testing R4-7: owner_email cannot be empty. The owner of the
      corresponding product must exist in the database.
    '''    
    # Case 1: owner is not in database
    users = User.query.all()
    testid = 0
    found_flag = False
    while not found_flag:
        for user in users:
            if user.id != testid:
                found_flag = True
                break
        if found_flag: 
            break
        testid += 1
    
    listing = create_listing('Title31', 'description of listing',
                             30.00, date(2021, 1, 3), testid)
    assert listing is None
    
    # Case 2: owner_email is not empty
    register('tu0', 'testtu0@test.com', '123456')
    user = User.query.filter_by(username='tu0').first()
    
    listing = create_listing('Title32', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is not None
    
    # Case 3: owner_email is empty
    user.email = ''  # Potential Bug? Need to use update_user_profile
    
    listing = create_listing('Title33', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is None


def test_r4_8_create_listing():
    '''
    Testing R4-8: A user cannot create products that have the same title.
    '''
    user = User.query.filter_by().first()
    
    # Case 1: Same Title
    listing = create_listing('Title41', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    listing = create_listing('Title41', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
        
    assert listing is None
    
    # Case 2: Different Title
    listing = create_listing('Title42', 'description of listing',
                             30.00, date(2021, 1, 3), user.id)
    assert listing is not None


def test_r5_1_update_listing():
    '''
    Testing R5-1: One can update all attributes of the listing,
    except owner_id and last_modified_date.
    '''
    listing = Listing.query.filter_by().first()

    # Test update title
    ntitle = "new title"
    assert (ntitle == listing.title) is False

    # Test whether listing.title got updated
    update_listing(listing, title=str(ntitle))
    assert (ntitle == listing.title) is True

    # Test update description
    long_description = "This is a detailed description with no grammar"
    assert (long_description == listing.description) is False

    # Test whether listing.description got updated
    update_listing(listing, description=str(long_description))
    assert (long_description == listing.description) is True

    # Test update price

    # Test price > 10000 constraint
    f = float(21000)
    assert update_listing(listing, price=f) is None

    # Test price < 10 constraint
    f = float(2)
    assert update_listing(listing, price=f) is None

    # Test whether listing.price got updated
    f = float(5000)
    assert update_listing(listing, price=f) is not None
    assert (float(5000) == listing.price) is True

    # Test multiple

    # Test update all three
    assert update_listing(listing, title="Three together",
                          description="There will be a total of three changes",
                          price=float(6000)) is not None

    # Check if update was implemented
    assert (listing.title == "Three together") is True
    assert (listing.description == "There will be a total of three changes")\
        is True
    assert (listing.price == 6000) is True

    # Test update all three, price fail
    assert update_listing(listing, title="Three together",
                          description="There will be a total of three changes",
                          price=float(500)) is None


def test_r5_2_update_listing():
    '''
    Testing R5-2: Price can be only increased but cannot be decreased :)
    '''
    listing = Listing.query.filter_by().first()

    # Check price decrease
    assert update_listing(listing, price=float(20)) is None
    assert (listing.price == 20) is False

    # Check price decrease
    assert update_listing(listing, price=float(6200)) is not None
    assert (listing.price == 6200) is True


def test_r5_3_update_listing():
    '''
    Testing R5-3: last_modified_date should be updated when 
    the update operation is successful.
    '''
    listing = Listing.query.filter_by().first()

    # Check modified date
    update_listing(listing, title=str("title2"))
    assert (listing.last_modified_date == date.today()) is True


def test_r5_4_update_listing():
    '''
    Testing R5-4: When updating an attribute, 
    one has to make sure that it follows the same requirements as above.
    '''
    listing = Listing.query.filter_by().first()

    # Title not alphanumeric
    assert update_listing(listing, title="%",
                          description="new stuff was written in here") is None

    # Space as prefix in title
    assert update_listing(listing, title=" title2",
                          description="new stuff was written in here") is None

    # Space as suffix in title
    assert update_listing(listing, title="title2 ",
                          description="new stuff was written in here") is None

    # Space as prefix and suffix in title
    assert update_listing(listing, title=" title2 ",
                          description="new stuff was written in here") is None

    # Space in middle of title
    assert update_listing(listing, title="ti tle2",
                          description="new stuff was written in") is not None

    # No Spaces
    assert update_listing(listing, title="title3",
                          description="new stuff was written in") is not None

    # Title less than 80 characters

    # 80 characters
    assert update_listing(listing, title='y' * 80) is not None

    # 81 characters
    assert update_listing(listing, title='y' * 81) is None

    # 5 characters
    assert update_listing(listing, title='y' * 5) is not None

    # Description no less than 20 characters and no greater than 2000
    # characters

    # 20 characters
    assert update_listing(listing, description='y' * 20) is not None

    # 19 characters
    assert update_listing(listing, description='y' * 19) is None

    # 2000 characters
    assert update_listing(listing, description='y' * 2000) is not None

    # 2001 characters
    assert update_listing(listing, description='y' * 2001) is None

    # Arbitrary numbers
    assert update_listing(listing, description='@*!&@ !@!+"{> :>>~ |":>DA>D')\
           is not None

    # Description must not be smaller than title

    # Smaller description than title
    short_description = "smo"
    assert update_listing(listing, description=short_description) is None

    # Larger description than title
    short_description = "This is a longer description then the other one"
    assert update_listing(listing, description=short_description) is not None

    # Price needs to in range [10, 10000], already did in r5-1

    # There can't be two listings with same title

    update_listing(listing, title="SAMETITLE")

    listing2 = Listing.query.filter_by(title="The Title62").first()

    # Same title case
    assert update_listing(listing2, title="SAMETITLE") is None

    # Different title case
    assert update_listing(listing2, title="Thishere") is not None
